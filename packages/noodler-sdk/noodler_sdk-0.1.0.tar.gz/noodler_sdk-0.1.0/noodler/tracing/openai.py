import json
import logging
from typing import Any, Dict, Iterator, List, Optional, Union
from opentelemetry.trace import Status, StatusCode

from .constants import (
    GEN_AI_INPUT_MESSAGES,
    GEN_AI_OPERATION_NAME,
    GEN_AI_OUTPUT_MESSAGES,
    GEN_AI_PROVIDER_NAME,
    GEN_AI_REQUEST_MAX_TOKENS,
    GEN_AI_REQUEST_MODEL,
    GEN_AI_REQUEST_TOP_P,
    GEN_AI_RESPONSE_FINISH_REASONS,
    GEN_AI_RESPONSE_ID,
    GEN_AI_RESPONSE_MODEL,
    GEN_AI_USAGE_INPUT_TOKENS,
    GEN_AI_USAGE_OUTPUT_TOKENS,
    GEN_AI_USAGE_TOTAL_TOKENS,
    MESSAGE_PART_TYPE_TEXT,
    OPERATION_CHAT,
    PROVIDER_OPENAI,
)
from .types import (
    Chat,
    ChatCompletionResponse,
    Completions,
    OpenAIClient,
)
from .utils import get_tracer

logger = logging.getLogger(__name__)


def _set_request_attributes(
    span: Any,
    model: str,
    max_tokens: Optional[int],
    top_p: Optional[float],
) -> None:
    """Set common request attributes on a span."""
    span.set_attribute(GEN_AI_PROVIDER_NAME, PROVIDER_OPENAI)
    span.set_attribute(GEN_AI_OPERATION_NAME, OPERATION_CHAT)
    span.set_attribute(GEN_AI_REQUEST_MODEL, model)

    if max_tokens is not None:
        span.set_attribute(GEN_AI_REQUEST_MAX_TOKENS, max_tokens)
    if top_p is not None:
        span.set_attribute(GEN_AI_REQUEST_TOP_P, top_p)


def _set_input_messages(
    span: Any,
    genai_input_messages: List[Dict[str, Any]],
) -> None:
    """Serialize and set input messages on a span."""
    try:
        span.set_attribute(GEN_AI_INPUT_MESSAGES, json.dumps(genai_input_messages))
    except (TypeError, ValueError) as e:
        logger.warning(f"Failed to serialize input messages: {e}")


def _set_usage_attributes(span: Any, usage: Any) -> None:
    """Set usage attributes on a span."""
    if not usage:
        return

    if hasattr(usage, "prompt_tokens") and usage.prompt_tokens is not None:
        span.set_attribute(GEN_AI_USAGE_INPUT_TOKENS, usage.prompt_tokens)
    if hasattr(usage, "completion_tokens") and usage.completion_tokens is not None:
        span.set_attribute(GEN_AI_USAGE_OUTPUT_TOKENS, usage.completion_tokens)
    if hasattr(usage, "total_tokens") and usage.total_tokens is not None:
        span.set_attribute(GEN_AI_USAGE_TOTAL_TOKENS, usage.total_tokens)

    logger.debug(
        f"Token usage - input: {getattr(usage, 'prompt_tokens', None)}, "
        f"output: {getattr(usage, 'completion_tokens', None)}, "
        f"total: {getattr(usage, 'total_tokens', None)}"
    )


class StreamingResponseWrapper:
    """Wrapper for streaming responses that adds tracing."""

    def __init__(
        self,
        stream: Iterator[ChatCompletionResponse],
        span: Any,
        model: str,
    ):
        self._stream = stream
        self._span = span
        self._model = model
        self._content_parts: List[str] = []
        self._response_id: Optional[str] = None
        self._response_model: Optional[str] = None
        self._finish_reason: Optional[str] = None
        self._usage: Optional[Any] = None
        self._first_chunk = True
        self._span_ended = False

    def _end_span(self) -> None:
        """End the span if not already ended."""
        if not self._span_ended:
            self._span.end()
            self._span_ended = True

    def __del__(self) -> None:
        """Safety net - end span if iterator was abandoned."""
        if not self._span_ended:
            try:
                logger.warning(
                    "Streaming iterator was abandoned before completion - ending span"
                )
            except Exception:
                # Logging may fail during interpreter shutdown
                pass
            self._end_span()

    def __iter__(self) -> Iterator[ChatCompletionResponse]:
        """Iterate over streaming chunks with tracing."""
        try:
            logger.debug("Starting to consume streaming response")
            for chunk in self._stream:
                # Extract metadata from first chunk
                if self._first_chunk:
                    self._response_id = getattr(chunk, "id", None)
                    self._response_model = getattr(chunk, "model", None)
                    if self._response_id:
                        self._span.set_attribute(GEN_AI_RESPONSE_ID, self._response_id)
                    if self._response_model:
                        self._span.set_attribute(
                            GEN_AI_RESPONSE_MODEL, self._response_model
                        )
                    self._first_chunk = False

                # Extract content from delta
                if hasattr(chunk, "choices") and chunk.choices:
                    choice = chunk.choices[0]
                    if hasattr(choice, "delta") and choice.delta:
                        delta = choice.delta
                        delta_content = getattr(delta, "content", None)
                        if delta_content:
                            self._content_parts.append(str(delta_content))

                    # Check for finish_reason (in last chunk)
                    finish_reason = getattr(choice, "finish_reason", None)
                    if finish_reason:
                        self._finish_reason = finish_reason

                # Extract usage (usually in last chunk)
                usage = getattr(chunk, "usage", None)
                if usage:
                    self._usage = usage

                yield chunk

            # Stream completed - set final attributes
            logger.debug("Streaming response completed")
            self._set_final_attributes()
            # End the span after stream completes
            self._end_span()

        except Exception as e:
            logger.error(f"Error during streaming: {e}", exc_info=True)
            self._span.record_exception(e)
            self._span.set_status(Status(StatusCode.ERROR, str(e)))
            self._end_span()
            raise

    def _set_final_attributes(self) -> None:
        """Set final span attributes after stream completes."""
        if self._finish_reason:
            self._span.set_attribute(
                GEN_AI_RESPONSE_FINISH_REASONS, [self._finish_reason]
            )

        # Format output messages
        full_content = "".join(self._content_parts)
        if full_content:
            genai_output_messages = [
                {
                    "role": "assistant",
                    "parts": [
                        {
                            "type": MESSAGE_PART_TYPE_TEXT,
                            "content": full_content,
                        }
                    ],
                    "finish_reason": self._finish_reason,
                }
            ]
            try:
                self._span.set_attribute(
                    GEN_AI_OUTPUT_MESSAGES, json.dumps(genai_output_messages)
                )
            except (TypeError, ValueError) as e:
                logger.warning(f"Failed to serialize output messages: {e}")

        # Set usage attributes
        _set_usage_attributes(self._span, self._usage)

        logger.debug(f"Streaming span completed successfully for model: {self._model}")


class WrappedCompletions:
    """Wrapper for OpenAI chat completions that adds tracing."""

    def __init__(self, inner: Completions):
        self._inner = inner

    def _build_api_kwargs(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        max_tokens: Optional[int],
        top_p: Optional[float],
        stream: bool = False,
        **extra: Any,
    ) -> Dict[str, Any]:
        """Build kwargs dict for OpenAI API call."""
        kwargs: Dict[str, Any] = {"model": model, "messages": messages, **extra}
        if stream:
            kwargs["stream"] = True
        if max_tokens is not None:
            kwargs["max_tokens"] = max_tokens
        if top_p is not None:
            kwargs["top_p"] = top_p
        return kwargs

    def create(
        self, **kwargs: Any
    ) -> Union[ChatCompletionResponse, Iterator[ChatCompletionResponse]]:
        # Extract request parameters
        model: str = kwargs.get("model", "unknown")
        messages: List[Dict[str, Any]] = kwargs.get("messages", [])
        max_tokens: Optional[int] = kwargs.get("max_tokens")
        top_p: Optional[float] = kwargs.get("top_p")
        stream: bool = kwargs.get("stream", False)

        # Validate message structure
        if not isinstance(messages, list):
            raise ValueError("messages must be a list")

        for i, msg in enumerate(messages):
            if not isinstance(msg, dict):
                raise ValueError(f"message at index {i} must be a dictionary")
            if "role" not in msg:
                raise ValueError(f"message at index {i} must have a 'role' field")
            # content is optional if tool_calls or function_call is present
            has_content = "content" in msg
            has_tool_calls = "tool_calls" in msg
            has_function_call = "function_call" in msg
            if not (has_content or has_tool_calls or has_function_call):
                raise ValueError(
                    f"message at index {i} must have 'content', 'tool_calls', or 'function_call'"
                )

        # Format input messages according to GenAI semantic conventions
        genai_input_messages = []
        for msg in messages:
            try:
                genai_input_messages.append(
                    {
                        "role": msg["role"],
                        "parts": [
                            {
                                "type": MESSAGE_PART_TYPE_TEXT,
                                "content": str(msg.get("content", "")),
                            }
                        ],
                    }
                )
            except (KeyError, TypeError) as e:
                logger.warning(f"Failed to format message: {e}")
                continue

        # Get tracer for this module
        tracer = get_tracer(__name__)
        logger.debug(
            f"Creating trace span for model: {model}, messages: {len(messages)}, stream={stream}"
        )

        # Create clean kwargs without already-extracted parameters
        clean_kwargs = {
            k: v
            for k, v in kwargs.items()
            if k not in ("model", "messages", "max_tokens", "top_p", "stream")
        }

        # Handle streaming responses
        if stream:
            return self._handle_streaming(
                tracer,
                model,
                genai_input_messages,
                max_tokens,
                top_p,
                messages,
                **clean_kwargs,
            )

        # Handle non-streaming responses
        return self._handle_non_streaming(
            tracer,
            model,
            genai_input_messages,
            max_tokens,
            top_p,
            messages,
            **clean_kwargs,
        )

    def _handle_streaming(
        self,
        tracer: Any,
        model: str,
        genai_input_messages: List[Dict[str, Any]],
        max_tokens: Optional[int],
        top_p: Optional[float],
        messages: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> Iterator[ChatCompletionResponse]:
        """Handle streaming responses with tracing."""
        # Create span that will stay open during streaming
        span = tracer.start_span(f"chat {model} (stream)")
        try:
            logger.debug(f"Span created for streaming: chat {model}")
            _set_request_attributes(span, model, max_tokens, top_p)
            _set_input_messages(span, genai_input_messages)

            # Build kwargs for API call
            api_kwargs = self._build_api_kwargs(
                model, messages, max_tokens, top_p, stream=True, **kwargs
            )

            # Make the actual API call
            logger.debug("Making OpenAI streaming API call")
            try:
                stream = self._inner.create(**api_kwargs)
                logger.debug("OpenAI streaming API call initiated")
            except Exception as e:
                logger.error(f"OpenAI streaming API call failed: {e}", exc_info=True)
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.end()
                raise

            # Wrap the stream with tracing
            wrapper = StreamingResponseWrapper(stream, span, model)
            return iter(wrapper)

        except Exception as e:
            # If span creation or setup fails, end the span and fall back
            if span.is_recording():
                span.record_exception(e)
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.end()
            logger.error(f"Failed to create trace span for streaming: {e}")
            # Fallback to untraced API call
            fallback_kwargs = self._build_api_kwargs(
                model, messages, max_tokens, top_p, stream=True, **kwargs
            )
            return self._inner.create(**fallback_kwargs)

    def _handle_non_streaming(
        self,
        tracer: Any,
        model: str,
        genai_input_messages: List[Dict[str, Any]],
        max_tokens: Optional[int],
        top_p: Optional[float],
        messages: List[Dict[str, Any]],
        **kwargs: Any,
    ) -> ChatCompletionResponse:
        """Handle non-streaming responses with tracing."""
        # Create span for the LLM interaction
        try:
            with tracer.start_as_current_span(f"chat {model}") as span:
                logger.debug(f"Span created: chat {model}")
                _set_request_attributes(span, model, max_tokens, top_p)
                _set_input_messages(span, genai_input_messages)

                # Build kwargs for API call
                api_kwargs = self._build_api_kwargs(
                    model, messages, max_tokens, top_p, **kwargs
                )

                # Make the actual API call
                logger.debug("Making OpenAI API call")
                try:
                    response = self._inner.create(**api_kwargs)
                    logger.debug("OpenAI API call completed successfully")
                except Exception as e:
                    # Record error in span
                    logger.error(f"OpenAI API call failed: {e}", exc_info=True)
                    span.record_exception(e)
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    raise

                # Validate response structure
                if not hasattr(response, "choices") or not response.choices:
                    error_msg = "Response has no choices"
                    span.set_status(Status(StatusCode.ERROR, error_msg))
                    logger.error(error_msg)
                    return response

                # Extract response information
                choice = response.choices[0]
                response_id = getattr(response, "id", None)
                response_model = getattr(response, "model", None)
                finish_reason = getattr(choice, "finish_reason", None)
                usage = getattr(response, "usage", None)

                # Format output messages according to GenAI semantic conventions
                genai_output_messages = []
                if hasattr(choice, "message") and choice.message:
                    message = choice.message
                    message_role = getattr(message, "role", None)
                    message_content = getattr(message, "content", None)

                    if message_role is not None and message_content is not None:
                        genai_output_messages.append(
                            {
                                "role": message_role,
                                "parts": [
                                    {
                                        "type": MESSAGE_PART_TYPE_TEXT,
                                        "content": str(message_content),
                                    }
                                ],
                                "finish_reason": finish_reason,
                            }
                        )

                # Set response attributes
                if response_id:
                    span.set_attribute(GEN_AI_RESPONSE_ID, response_id)
                if response_model:
                    span.set_attribute(GEN_AI_RESPONSE_MODEL, response_model)
                if finish_reason:
                    span.set_attribute(GEN_AI_RESPONSE_FINISH_REASONS, [finish_reason])

                # Set output messages (serialized as JSON string)
                if genai_output_messages:
                    try:
                        span.set_attribute(
                            GEN_AI_OUTPUT_MESSAGES, json.dumps(genai_output_messages)
                        )
                    except (TypeError, ValueError) as e:
                        logger.warning(f"Failed to serialize output messages: {e}")

                # Set usage attributes
                _set_usage_attributes(span, usage)

                logger.debug(f"Span completed successfully for model: {model}")
                return response
        except Exception as e:
            # If span creation fails, still make the API call but log the error
            logger.error(f"Failed to create trace span: {e}")
            # Fallback to untraced API call
            fallback_kwargs = self._build_api_kwargs(
                model, messages, max_tokens, top_p, **kwargs
            )
            return self._inner.create(**fallback_kwargs)


class WrappedChat:
    """Wrapper for OpenAI chat that provides traced completions."""

    def __init__(self, inner: Chat):
        self._inner = inner

    @property
    def completions(self) -> WrappedCompletions:
        return WrappedCompletions(self._inner.completions)


class WrappedOpenAI:
    """Wrapper for OpenAI client that provides traced chat completions."""

    def __init__(self, inner: OpenAIClient):
        self._inner = inner

    @property
    def chat(self) -> WrappedChat:
        return WrappedChat(self._inner.chat)


def instrument_openai(client: OpenAIClient) -> WrappedOpenAI:
    """Instrument an OpenAI client to automatically trace API calls.

    This function wraps the OpenAI client to automatically trace API calls.
    Currently, only the `chat.completions.create()` method is supported.
    Both streaming and non-streaming responses are traced.
    Other OpenAI endpoints (embeddings, audio, etc.) are not instrumented.

    Args:
        client: The OpenAI client instance to instrument.

    Returns:
        A wrapped OpenAI client that traces all API calls.

    Example:
        >>> from openai import OpenAI
        >>> from noodler import instrument_openai
        >>> client = OpenAI()
        >>> wrapped_client = instrument_openai(client)
        >>> # Non-streaming
        >>> response = wrapped_client.chat.completions.create(...)
        >>> # Streaming
        >>> stream = wrapped_client.chat.completions.create(..., stream=True)
        >>> for chunk in stream:
        ...     print(chunk)
    """
    logger.info("Instrumenting OpenAI client for tracing")
    wrapped = WrappedOpenAI(client)
    logger.debug("OpenAI client instrumentation completed")
    return wrapped
