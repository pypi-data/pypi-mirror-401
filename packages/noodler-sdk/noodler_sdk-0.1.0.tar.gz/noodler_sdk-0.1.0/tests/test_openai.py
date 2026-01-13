from unittest.mock import Mock
import pytest

from noodler.tracing.openai import (
    StreamingResponseWrapper,
    WrappedCompletions,
    WrappedOpenAI,
    instrument_openai,
)


class MockCompletions:
    """Mock OpenAI completions interface."""

    def __init__(self):
        self.create_called = False
        self.create_kwargs = None

    def create(self, **kwargs):
        """Mock create method."""
        self.create_called = True
        self.create_kwargs = kwargs

        # Create a mock response
        response = Mock()
        response.id = "test-id"
        response.model = "gpt-3.5-turbo"
        response.choices = [Mock()]
        response.choices[0].message = Mock()
        response.choices[0].message.role = "assistant"
        response.choices[0].message.content = "Test response"
        response.choices[0].finish_reason = "stop"
        response.usage = Mock()
        response.usage.prompt_tokens = 10
        response.usage.completion_tokens = 20
        response.usage.total_tokens = 30
        return response


class MockChat:
    """Mock OpenAI chat interface."""

    def __init__(self):
        self.completions = MockCompletions()


class MockOpenAIClient:
    """Mock OpenAI client."""

    def __init__(self):
        self.chat = MockChat()


def test_instrument_openai():
    """Test instrumenting an OpenAI client."""
    client = MockOpenAIClient()
    wrapped = instrument_openai(client)

    assert isinstance(wrapped, WrappedOpenAI)
    assert wrapped._inner == client


def test_wrapped_completions_create_valid_messages():
    """Test WrappedCompletions.create with valid messages."""
    mock_completions = MockCompletions()
    wrapped = WrappedCompletions(mock_completions)

    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]

    response = wrapped.create(model="gpt-3.5-turbo", messages=messages)

    assert mock_completions.create_called
    assert response.id == "test-id"
    assert response.model == "gpt-3.5-turbo"


def test_wrapped_completions_create_invalid_messages_not_list():
    """Test WrappedCompletions.create with messages that are not a list."""
    mock_completions = MockCompletions()
    wrapped = WrappedCompletions(mock_completions)

    with pytest.raises(ValueError, match="must be a list"):
        wrapped.create(model="gpt-3.5-turbo", messages="not a list")


def test_wrapped_completions_create_invalid_message_not_dict():
    """Test WrappedCompletions.create with message that is not a dict."""
    mock_completions = MockCompletions()
    wrapped = WrappedCompletions(mock_completions)

    with pytest.raises(ValueError, match="must be a dictionary"):
        wrapped.create(model="gpt-3.5-turbo", messages=["not a dict"])


def test_wrapped_completions_create_missing_role():
    """Test WrappedCompletions.create with message missing role."""
    mock_completions = MockCompletions()
    wrapped = WrappedCompletions(mock_completions)

    with pytest.raises(ValueError, match="must have a 'role' field"):
        wrapped.create(
            model="gpt-3.5-turbo",
            messages=[{"content": "Hello"}],
        )


def test_wrapped_completions_create_missing_content():
    """Test WrappedCompletions.create with message missing content, tool_calls, and function_call."""
    mock_completions = MockCompletions()
    wrapped = WrappedCompletions(mock_completions)

    with pytest.raises(
        ValueError, match="must have 'content', 'tool_calls', or 'function_call'"
    ):
        wrapped.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user"}],
        )


def test_wrapped_completions_create_with_tool_calls():
    """Test WrappedCompletions.create with message that has tool_calls instead of content."""
    mock_completions = MockCompletions()
    wrapped = WrappedCompletions(mock_completions)

    messages = [
        {"role": "user", "content": "What's the weather?"},
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {"name": "get_weather", "arguments": "{}"},
                }
            ],
        },
    ]

    # Should not raise - tool_calls is a valid alternative to content
    response = wrapped.create(model="gpt-3.5-turbo", messages=messages)
    assert mock_completions.create_called


def test_wrapped_completions_create_empty_choices():
    """Test WrappedCompletions.create with response that has no choices."""
    mock_completions = MockCompletions()

    # Override create to return response with no choices
    def create_no_choices(**kwargs):
        response = Mock()
        response.choices = []
        return response

    mock_completions.create = create_no_choices
    wrapped = WrappedCompletions(mock_completions)

    messages = [{"role": "user", "content": "Hello"}]
    response = wrapped.create(model="gpt-3.5-turbo", messages=messages)

    # Should return response even if no choices
    assert response.choices == []


def test_wrapped_completions_create_with_max_tokens():
    """Test WrappedCompletions.create with max_tokens parameter."""
    mock_completions = MockCompletions()
    wrapped = WrappedCompletions(mock_completions)

    messages = [{"role": "user", "content": "Hello"}]
    wrapped.create(model="gpt-3.5-turbo", messages=messages, max_tokens=100)

    assert mock_completions.create_called
    assert mock_completions.create_kwargs["max_tokens"] == 100


def test_wrapped_completions_create_with_top_p():
    """Test WrappedCompletions.create with top_p parameter."""
    mock_completions = MockCompletions()
    wrapped = WrappedCompletions(mock_completions)

    messages = [{"role": "user", "content": "Hello"}]
    wrapped.create(model="gpt-3.5-turbo", messages=messages, top_p=0.9)

    assert mock_completions.create_called
    assert mock_completions.create_kwargs["top_p"] == 0.9


def test_wrapped_completions_create_api_error():
    """Test WrappedCompletions.create when API call fails."""
    mock_completions = MockCompletions()

    # Override create to raise an exception
    def create_error(**kwargs):
        raise Exception("API error")

    mock_completions.create = create_error
    wrapped = WrappedCompletions(mock_completions)

    messages = [{"role": "user", "content": "Hello"}]

    with pytest.raises(Exception, match="API error"):
        wrapped.create(model="gpt-3.5-turbo", messages=messages)


# --- Streaming Tests ---


def create_mock_streaming_chunk(
    chunk_id="test-id",
    model="gpt-3.5-turbo",
    delta_content=None,
    finish_reason=None,
    usage=None,
):
    """Helper to create a mock streaming chunk."""
    chunk = Mock()
    chunk.id = chunk_id
    chunk.model = model
    chunk.choices = [Mock()]
    chunk.choices[0].delta = Mock()
    chunk.choices[0].delta.content = delta_content
    chunk.choices[0].finish_reason = finish_reason
    chunk.usage = usage
    return chunk


def create_mock_stream(chunks):
    """Create a mock stream iterator from a list of chunks."""
    return iter(chunks)


class MockStreamingCompletions:
    """Mock OpenAI completions interface that returns streaming responses."""

    def __init__(self, chunks):
        self.chunks = chunks
        self.create_called = False
        self.create_kwargs = None

    def create(self, **kwargs):
        """Mock create method returning an iterator."""
        self.create_called = True
        self.create_kwargs = kwargs
        return iter(self.chunks)


def test_streaming_response_wrapper_iterates_chunks():
    """Test that StreamingResponseWrapper yields all chunks."""
    chunks = [
        create_mock_streaming_chunk(delta_content="Hello"),
        create_mock_streaming_chunk(delta_content=" world"),
        create_mock_streaming_chunk(delta_content="!", finish_reason="stop"),
    ]

    mock_span = Mock()
    mock_span.is_recording.return_value = True

    wrapper = StreamingResponseWrapper(
        stream=iter(chunks),
        span=mock_span,
        model="gpt-3.5-turbo",
    )

    collected = list(wrapper)

    assert len(collected) == 3
    assert collected[0].choices[0].delta.content == "Hello"
    assert collected[1].choices[0].delta.content == " world"
    assert collected[2].choices[0].delta.content == "!"


def test_streaming_response_wrapper_sets_response_attributes():
    """Test that StreamingResponseWrapper sets span attributes from first chunk."""
    chunks = [
        create_mock_streaming_chunk(
            chunk_id="resp-123", model="gpt-4", delta_content="Hi"
        ),
    ]

    mock_span = Mock()
    mock_span.is_recording.return_value = True

    wrapper = StreamingResponseWrapper(
        stream=iter(chunks),
        span=mock_span,
        model="gpt-4",
    )

    list(wrapper)  # Consume the stream

    # Check that response ID and model were set
    mock_span.set_attribute.assert_any_call("gen_ai.response.id", "resp-123")
    mock_span.set_attribute.assert_any_call("gen_ai.response.model", "gpt-4")


def test_streaming_response_wrapper_sets_finish_reason():
    """Test that StreamingResponseWrapper sets finish_reason attribute."""
    chunks = [
        create_mock_streaming_chunk(delta_content="Hello"),
        create_mock_streaming_chunk(finish_reason="stop"),
    ]

    mock_span = Mock()
    mock_span.is_recording.return_value = True

    wrapper = StreamingResponseWrapper(
        stream=iter(chunks),
        span=mock_span,
        model="gpt-3.5-turbo",
    )

    list(wrapper)

    mock_span.set_attribute.assert_any_call("gen_ai.response.finish_reasons", ["stop"])


def test_streaming_response_wrapper_sets_usage():
    """Test that StreamingResponseWrapper sets usage attributes from last chunk."""
    usage = Mock()
    usage.prompt_tokens = 10
    usage.completion_tokens = 20
    usage.total_tokens = 30

    chunks = [
        create_mock_streaming_chunk(delta_content="Hello"),
        create_mock_streaming_chunk(finish_reason="stop", usage=usage),
    ]

    mock_span = Mock()
    mock_span.is_recording.return_value = True

    wrapper = StreamingResponseWrapper(
        stream=iter(chunks),
        span=mock_span,
        model="gpt-3.5-turbo",
    )

    list(wrapper)

    mock_span.set_attribute.assert_any_call("gen_ai.usage.input_tokens", 10)
    mock_span.set_attribute.assert_any_call("gen_ai.usage.output_tokens", 20)
    mock_span.set_attribute.assert_any_call("gen_ai.usage.total_tokens", 30)


def test_streaming_response_wrapper_ends_span():
    """Test that StreamingResponseWrapper ends span after iteration."""
    chunks = [create_mock_streaming_chunk(delta_content="Hi", finish_reason="stop")]

    mock_span = Mock()
    mock_span.is_recording.return_value = True

    wrapper = StreamingResponseWrapper(
        stream=iter(chunks),
        span=mock_span,
        model="gpt-3.5-turbo",
    )

    list(wrapper)

    mock_span.end.assert_called_once()


def test_streaming_response_wrapper_handles_error():
    """Test that StreamingResponseWrapper handles errors during streaming."""

    def error_stream():
        yield create_mock_streaming_chunk(delta_content="Hello")
        raise Exception("Stream error")

    mock_span = Mock()
    mock_span.is_recording.return_value = True

    wrapper = StreamingResponseWrapper(
        stream=error_stream(),
        span=mock_span,
        model="gpt-3.5-turbo",
    )

    with pytest.raises(Exception, match="Stream error"):
        list(wrapper)

    mock_span.record_exception.assert_called_once()
    mock_span.set_status.assert_called_once()
    mock_span.end.assert_called_once()


def test_wrapped_completions_streaming_create():
    """Test WrappedCompletions.create with stream=True."""
    chunks = [
        create_mock_streaming_chunk(delta_content="Hello"),
        create_mock_streaming_chunk(delta_content=" world", finish_reason="stop"),
    ]

    mock_completions = MockStreamingCompletions(chunks)
    wrapped = WrappedCompletions(mock_completions)

    messages = [{"role": "user", "content": "Hi"}]
    stream = wrapped.create(model="gpt-3.5-turbo", messages=messages, stream=True)

    # Should return an iterator
    collected = list(stream)

    assert mock_completions.create_called
    assert mock_completions.create_kwargs["stream"] is True
    assert len(collected) == 2


def test_wrapped_completions_streaming_api_error():
    """Test WrappedCompletions.create with stream=True when API call fails."""
    mock_completions = MockStreamingCompletions([])

    def create_error(**kwargs):
        raise Exception("Streaming API error")

    mock_completions.create = create_error
    wrapped = WrappedCompletions(mock_completions)

    messages = [{"role": "user", "content": "Hello"}]

    with pytest.raises(Exception, match="Streaming API error"):
        wrapped.create(model="gpt-3.5-turbo", messages=messages, stream=True)
