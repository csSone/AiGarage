"""Chat completions router for the model server proxy."""

import json
from typing import AsyncGenerator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..config import settings
from ..providers import OpenAIProvider, AnthropicProvider, GoogleProvider, ZaiProvider
from ..providers.base import ChatRequest, ChatResponse, StreamChunk

router = APIRouter(prefix="/v1", tags=["chat"])

# Provider instances
_providers = {
    "openai": OpenAIProvider(
        api_key=settings.openai_api_key, base_url=settings.openai_base_url
    ),
    "anthropic": AnthropicProvider(
        api_key=settings.anthropic_api_key, base_url=settings.anthropic_base_url
    ),
    "google": GoogleProvider(api_key=settings.google_api_key),
    "zai": ZaiProvider(api_key=settings.zai_api_key, base_url=settings.zai_base_url),
}


class ProviderChatRequest(ChatRequest):
    """Chat request with provider specification."""

    provider: str = Field(
        ...,
        description="AI provider to use: 'openai', 'anthropic', 'google', or 'zai'",
    )


@router.post("/chat/completions")
async def chat_completions(request: Request, raw_request: dict):
    """Handle chat completion requests.

    This endpoint provides an OpenAI-compatible interface that routes
    requests to the appropriate AI provider based on the 'provider' parameter.

    Request format:
    {
        "provider": "openai" | "anthropic" | "google" | "zai",
        "model": "model-name",
        "messages": [{"role": "user", "content": "..."}],
        "stream": true | false,
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 1.0
    }
    """
    try:
        # Parse request
        chat_request = ProviderChatRequest(**raw_request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid request: {e}")

    # Get provider
    provider = _providers.get(chat_request.provider)
    if not provider:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown provider: {chat_request.provider}. "
            f"Valid options: {', '.join(_providers.keys())}",
        )

    # Handle request
    try:
        result = await provider.chat_completions(chat_request)

        if chat_request.stream:
            # Streaming response
            return StreamingResponse(
                _stream_formatter(result, chat_request.model),
                media_type="text/event-stream",
            )
        else:
            # Non-streaming response
            return result.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider error: {e}")


async def _stream_formatter(
    stream: AsyncGenerator[StreamChunk, None], model: str
) -> AsyncGenerator[str, None]:
    """Format streaming chunks as Server-Sent Events.

    Args:
        stream: Async generator of stream chunks
        model: Model name for the response

    Yields:
        SSE-formatted strings
    """
    async for chunk in stream:
        data = chunk.model_dump()
        yield f"data: {json.dumps(data)}\n\n"

    # Send final [DONE] message
    yield "data: [DONE]\n\n"
