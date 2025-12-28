"""OpenAI provider implementation."""

import json
from typing import AsyncGenerator

from openai import AsyncOpenAI

from .base import (
    BaseProvider,
    ChatRequest,
    ChatResponse,
    ChatChoice,
    StreamChunk,
    Usage,
)


class OpenAIProvider(BaseProvider):
    """OpenAI API provider implementation.

    Uses the official OpenAI Python SDK with async support.
    """

    def __init__(self, api_key: str, base_url: str | None = None):
        """Initialize the OpenAI provider.

        Args:
            api_key: OpenAI API key
            base_url: Optional custom base URL (for proxies/compatibility layers)
        """
        super().__init__(api_key, base_url)
        client_kwargs = {"api_key": api_key}
        if base_url:
            client_kwargs["base_url"] = base_url
        self._client = AsyncOpenAI(**client_kwargs)

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
        # Convert Pydantic models to dicts for OpenAI SDK
        messages = [msg.model_dump() for msg in request.messages]

        kwargs = {
            "model": request.model,
            "messages": messages,
            "temperature": request.temperature,
            "top_p": request.top_p,
        }

        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens

        if request.stream:
            return self._stream_response(request, **kwargs)
        else:
            return await self._non_stream_response(request, **kwargs)

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
        response = await self._client.chat.completions.create(**kwargs)

        return ChatResponse(
            id=response.id,
            created=int(response.created),
            model=response.model,
            choices=[
                ChatChoice(
                    index=choice.index,
                    message={
                        "role": choice.message.role,
                        "content": choice.message.content,
                    },
                    finish_reason=choice.finish_reason,
                )
                for choice in response.choices
            ],
            usage=Usage(
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens,
                total_tokens=response.usage.total_tokens,
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
        kwargs["stream"] = True
        stream = await self._client.chat.completions.create(**kwargs)

        async for chunk in stream:
            if not chunk.choices:
                continue

            choices = []
            for choice in chunk.choices:
                delta = {}
                if choice.delta.role:
                    delta["role"] = choice.delta.role
                if choice.delta.content:
                    delta["content"] = choice.delta.content

                choices.append(
                    {
                        "index": choice.index,
                        "delta": delta,
                        "finish_reason": choice.finish_reason,
                    }
                )

            yield StreamChunk(
                id=chunk.id,
                created=int(chunk.created),
                model=chunk.model,
                choices=choices,
            )
