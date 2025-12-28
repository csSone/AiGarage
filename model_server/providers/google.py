"""Google AI (Gemini) provider implementation."""

from typing import AsyncGenerator

import google.generativeai as genai

from .base import (
    BaseProvider,
    ChatRequest,
    ChatResponse,
    ChatChoice,
    StreamChunk,
    Usage,
)


class GoogleProvider(BaseProvider):
    """Google AI (Gemini) provider implementation.

    Uses the official Google GenerativeAI SDK.
    Converts between OpenAI and Google AI request/response formats.
    """

    def __init__(self, api_key: str, base_url: str | None = None):
        """Initialize the Google AI provider.

        Args:
            api_key: Google AI API key
            base_url: Not used for Google AI (kept for interface consistency)
        """
        super().__init__(api_key, base_url)
        genai.configure(api_key=api_key)

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
        # Transform OpenAI format to Google AI format
        model = genai.GenerativeModel(request.model)

        # Combine messages into a single prompt for Gemini
        prompt = self._transform_messages(request.messages)

        generation_config = genai.types.GenerationConfig(
            temperature=request.temperature,
            top_p=request.top_p,
            max_output_tokens=request.max_tokens,
        )

        if request.stream:
            return self._stream_response(request, model, prompt, generation_config)
        else:
            return await self._non_stream_response(
                request, model, prompt, generation_config
            )

    def _transform_messages(self, messages: list) -> str:
        """Transform OpenAI message format to Google AI format.

        Args:
            messages: List of messages in OpenAI format

        Returns:
            Formatted prompt string for Gemini
        """
        parts = []
        for msg in messages:
            if msg.role == "system":
                parts.append(f"System: {msg.content}\n")
            elif msg.role == "user":
                parts.append(f"User: {msg.content}\n")
            elif msg.role == "assistant":
                parts.append(f"Assistant: {msg.content}\n")

        return "".join(parts)

    async def _non_stream_response(
        self,
        request: ChatRequest,
        model: genai.GenerativeModel,
        prompt: str,
        generation_config: genai.types.GenerationConfig,
    ) -> ChatResponse:
        """Handle non-streaming response.

        Args:
            request: Original chat request
            model: Gemini model instance
            prompt: Formatted prompt
            generation_config: Generation configuration

        Returns:
            ChatResponse in OpenAI format
        """
        response = await model.generate_content_async(
            prompt, generation_config=generation_config
        )

        content = response.text

        # Estimate token usage (Gemini doesn't provide exact counts)
        # Rough estimate: ~4 characters per token
        prompt_tokens = len(prompt) // 4
        completion_tokens = len(content) // 4

        return ChatResponse(
            id=self._generate_id(),
            created=self._get_timestamp(),
            model=request.model,
            choices=[
                ChatChoice(
                    index=0,
                    message={"role": "assistant", "content": content},
                    finish_reason="stop",
                )
            ],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            ),
        )

    async def _stream_response(
        self,
        request: ChatRequest,
        model: genai.GenerativeModel,
        prompt: str,
        generation_config: genai.types.GenerationConfig,
    ) -> AsyncGenerator[StreamChunk, None]:
        """Handle streaming response.

        Args:
            request: Original chat request
            model: Gemini model instance
            prompt: Formatted prompt
            generation_config: Generation configuration

        Yields:
            StreamChunk for each piece of the response
        """
        response_id = self._generate_id()
        created = self._get_timestamp()

        stream = await model.generate_content_async(
            prompt, generation_config=generation_config, stream=True
        )

        async for chunk in stream:
            content = chunk.text
            if content:
                yield StreamChunk(
                    id=response_id,
                    created=created,
                    model=request.model,
                    choices=[
                        {
                            "index": 0,
                            "delta": {"content": content},
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
