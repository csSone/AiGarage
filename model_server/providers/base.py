"""Abstract base class for AI provider implementations."""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Dict, Any

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Chat message format (OpenAI-compatible)."""
    role: str
    content: str


class ChatRequest(BaseModel):
    """Chat completion request format (OpenAI-compatible)."""
    model: str
    messages: list[ChatMessage]
    temperature: float | None = 0.7
    max_tokens: int | None = None
    top_p: float | None = 1.0
    stream: bool = False


class ChatChoice(BaseModel):
    """Chat completion choice."""
    index: int
    message: Dict[str, Any]
    finish_reason: str


class Usage(BaseModel):
    """Token usage information."""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatResponse(BaseModel):
    """Chat completion response format (OpenAI-compatible)."""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: list[ChatChoice]
    usage: Usage


class StreamChunk(BaseModel):
    """Streaming response chunk format."""
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: list[Dict[str, Any]]


class BaseProvider(ABC):
    """Abstract base class for AI provider implementations.

    All providers must implement the chat_completions method to handle
    both streaming and non-streaming requests in OpenAI-compatible format.
    """

    def __init__(self, api_key: str, base_url: str | None = None):
        """Initialize the provider.

        Args:
            api_key: API key for the provider
            base_url: Optional custom base URL for the provider API
        """
        self.api_key = api_key
        self.base_url = base_url

    @abstractmethod
    async def chat_completions(
        self,
        request: ChatRequest,
    ) -> ChatResponse | AsyncGenerator[StreamChunk, None]:
        """Handle chat completion request.

        Args:
            request: Chat completion request in OpenAI format

        Returns:
            - ChatResponse for non-streaming requests
            - AsyncGenerator[StreamChunk] for streaming requests

        Raises:
            Exception: Provider-specific errors
        """
        pass

    def _generate_id(self) -> str:
        """Generate a unique ID for the response."""
        import uuid
        return f"chatcmpl-{uuid.uuid4().hex[:24]}"

    def _get_timestamp(self) -> int:
        """Get current timestamp."""
        import time
        return int(time.time())
