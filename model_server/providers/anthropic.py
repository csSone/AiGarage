"""Anthropic (Claude) provider implementation."""

import uuid
from typing import AsyncGenerator

from anthropic import AsyncAnthropic

from .base import (
    BaseProvider,
    ChatRequest,
    ChatResponse,
    ChatChoice,
    StreamChunk,
    Usage,
)


class AnthropicProvider(BaseProvider):
    """Anthropic Claude API provider implementation.

    Uses the official Anthropic Python SDK with async support.
    Converts between OpenAI and Anthropic request/response formats.
    """

    def __init__(self, api_key: str, base_url: str | None = None):
        """Initialize the Anthropic provider.

        Args:
            api_key: Anthropic API key
            base_url: Optional custom base URL (for proxies/compatibility layers)
        """
        super().__init__(api_key, base_url)
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self._client = AsyncAnthropic(**client_kwargs)

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
        """
        # Transform OpenAI format to Anthropic format
        messages = self._transform_messages(request.messages)

        kwargs = {
            "model": request.model,
            "messages": messages,
            "max_tokens": request.max_tokens or 4096,
            "temperature": request.temperature,
            "top_p": request.top_p,
        }

        if request.stream:
            return self._stream_response(request, **kwargs)
        else:
            return await self._non_stream_response(request, **kwargs)

    def _transform_messages(self, messages: list) -> list[dict]:
        """Transform OpenAI message format to Anthropic format.

        Anthropic requires the first message to be a 'user' role and
        handles system messages separately.

        Args:
            messages: List of messages in OpenAI format

        Returns:
            List of messages in Anthropic format
        """
        anthropic_messages = []

        for msg in messages:
            if msg.role == "system":
                # Anthropic handles system messages as a separate parameter
                # We'll prepend this content to the first user message
                continue
            elif msg.role == "assistant":
                anthropic_messages.append({"role": "assistant", "content": msg.content})
            else:  # user
                anthropic_messages.append({"role": "user", "content": msg.content})

        return anthropic_messages

    async def _non_stream_response(
        self,
        request: ChatRequest,
        **kwargs,
    ) -> ChatResponse:
        """Handle non-streaming response.

        Args:
            request: Original chat request
            **kwargs: Additional parameters for the API call

        Returns:
            ChatResponse in OpenAI format
        """
        response = await self._client.messages.create(**kwargs)

        # Extract content from Anthropic response
        content = ""
        for block in response.content:
            if block.type == "text":
                content += block.text

        return ChatResponse(
            id=self._generate_id(),
            created=self._get_timestamp(),
            model=response.model,
            choices=[
                ChatChoice(
                    index=0,
                    message={"role": "assistant", "content": content},
                    finish_reason=response.stop_reason,
                )
            ],
            usage=Usage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            ),
        )

    async def _stream_response(
        self,
        request: ChatRequest,
        **kwargs,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Handle streaming response.

        Args:
            request: Original chat request
            **kwargs: Additional parameters for the API call

        Yields:
            StreamChunk for each piece of the response
        """
        response_id = self._generate_id()
        created = self._get_timestamp()

        async with self._client.messages.stream(**kwargs) as stream:
            async for text in stream.text_stream:
                yield StreamChunk(
                    id=response_id,
                    created=created,
                    model=request.model,
                    choices=[
                        {
                            "index": 0,
                            "delta": {"content": text},
                            "finish_reason": None,
                        }
                    ],
                )

            # Send final chunk with finish_reason
            yield StreamChunk(
                id=response_id,
                created=created,
                model=request.model,
                choices=[
                    {
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop",
                    }
                ],
            )
