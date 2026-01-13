from typing import Any, Iterator, List, Optional, Protocol, Union


class ChatMessage(Protocol):
    """Protocol for a chat message in OpenAI format."""

    role: str
    content: str


class Usage(Protocol):
    """Protocol for OpenAI usage information."""

    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]


class ChoiceMessage(Protocol):
    """Protocol for a message in a choice."""

    role: str
    content: Optional[str]


class ChoiceDelta(Protocol):
    """Protocol for a delta in a streaming choice."""

    role: Optional[str]
    content: Optional[str]


class Choice(Protocol):
    """Protocol for a choice in OpenAI response."""

    message: ChoiceMessage
    finish_reason: Optional[str]
    delta: Optional[ChoiceDelta]  # For streaming responses


class ChatCompletionResponse(Protocol):
    """Protocol for OpenAI chat completion response."""

    id: str
    model: str
    choices: List[Choice]
    usage: Optional[Usage]


class Completions(Protocol):
    """Protocol for OpenAI completions interface."""

    def create(
        self, **kwargs: Any
    ) -> Union[ChatCompletionResponse, Iterator[ChatCompletionResponse]]:
        """Create a chat completion.

        Returns ChatCompletionResponse if stream=False (default),
        or Iterator[ChatCompletionResponse] if stream=True.
        """
        ...


class Chat(Protocol):
    """Protocol for OpenAI chat interface."""

    @property
    def completions(self) -> Completions:
        """Get completions interface."""
        ...


class OpenAIClient(Protocol):
    """Protocol for OpenAI client interface."""

    @property
    def chat(self) -> Chat:
        """Get chat interface."""
        ...
