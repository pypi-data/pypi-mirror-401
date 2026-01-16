"""
Unified Text Client for Unified AI SDK.

Provides LLM text generation capabilities with:
- Multi-provider support (Gemini, OpenAI, Anthropic)
- Fallback chain with breadcrumb tracking
- JSON/structured output mode (response_format)
- Streaming support
"""

import time
from typing import Any, AsyncIterator, Dict, List, Optional

from ..breadcrumbs import add_error, add_info, add_success, add_warning, SDKLayer
from ..exceptions import AllProvidersFailedError, ProviderError
from ..models import TextRequest, TextResponse
from .base import AdapterRegistry, BaseCapabilityClient


class UnifiedTextClient(BaseCapabilityClient[TextRequest, TextResponse]):
    """
    Unified LLM client with multi-provider fallback support.

    Features:
        - Execute LLM on specific provider/model
        - Automatic fallback through provider chain
        - JSON structured output mode (response_format)
        - Full breadcrumb tracking

    Example:
        client = UnifiedTextClient(registry=registry, fallback_chain=[...])
        request = TextRequest(
            prompt="Extract name from: John Smith is 30",
            response_format={"type": "json_object"}
        )
        response = await client.execute(request, "gemini/gemini-2.0-flash")
    """

    CAPABILITY: str = "text"

    async def execute(self, request: TextRequest, model: str) -> TextResponse:
        """
        Execute LLM on specific model.

        Args:
            request: Text request with prompt, messages, response_format, etc.
            model: Model string in "provider/model" format

        Returns:
            TextResponse with content and metadata

        Raises:
            ValueError: If model string is invalid
            ProviderError: If provider call fails
        """
        start_time = time.time()
        provider, model_name = self._parse_model_string(model)

        adapter = self.registry.get_for_model(model)

        add_info(
            layer=SDKLayer.CLIENT.value,
            action="text_execute_start",
            message=f"Executing LLM with {provider}/{model_name}",
            provider=provider,
            model=model_name,
            has_json_mode=request.response_format is not None,
        )

        # Build kwargs from request - NO hardcoding, pass through all params
        kwargs: Dict[str, Any] = {}
        if request.temperature is not None:
            kwargs["temperature"] = request.temperature
        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens
        if request.top_p is not None:
            kwargs["top_p"] = request.top_p
        if request.stop is not None:
            kwargs["stop"] = request.stop
        if request.response_format is not None:
            kwargs["response_format"] = request.response_format
        if request.tools is not None:
            kwargs["tools"] = request.tools
        if request.tool_choice is not None:
            kwargs["tool_choice"] = request.tool_choice
        if request.provider_params:
            kwargs.update(request.provider_params)

        # Convert prompt to messages if needed
        messages = request.messages
        if messages is None and request.prompt:
            messages = [{"role": "user", "content": request.prompt}]
            if request.system:
                messages.insert(0, {"role": "system", "content": request.system})

        if not messages:
            raise ValueError("Either 'messages' or 'prompt' must be provided")

        result = await adapter.complete(
            messages=messages,
            model=model_name,
            **kwargs,
        )

        latency_ms = (time.time() - start_time) * 1000

        add_success(
            layer=SDKLayer.CLIENT.value,
            action="text_execute_complete",
            message=f"LLM completed with {provider}/{model_name}",
            provider=provider,
            model=model_name,
            latency_ms=latency_ms,
            content_length=len(result.get("content", "")),
        )

        return TextResponse(
            success=True,
            provider=provider,
            model=model_name,
            latency_ms=latency_ms,
            content=result.get("content", ""),
            finish_reason=result.get("finish_reason"),
            tool_calls=result.get("tool_calls"),
            usage=result.get("usage", {}),
        )

    async def execute_with_fallback(self, request: TextRequest) -> TextResponse:
        """
        Execute LLM with automatic fallback through provider chain.

        Args:
            request: Text request

        Returns:
            TextResponse from first successful provider

        Raises:
            AllProvidersFailedError: If all providers fail
        """
        errors = []

        for model in self.fallback_chain:
            try:
                add_info(
                    layer=SDKLayer.CLIENT.value,
                    action="text_fallback_attempt",
                    message=f"Attempting LLM with {model}",
                    model=model,
                )
                return await self.execute(request, model)
            except ProviderError as e:
                errors.append({"model": model, "error": str(e)})
                add_warning(
                    layer=SDKLayer.CLIENT.value,
                    action="text_fallback_failed",
                    message=f"Provider {model} failed, trying next",
                    model=model,
                    error=str(e),
                )

        add_error(
            layer=SDKLayer.CLIENT.value,
            action="text_all_providers_failed",
            message="All text providers failed",
            errors=errors,
        )

        raise AllProvidersFailedError(
            message="All text providers failed",
            errors=errors,
        )

    async def stream(
        self,
        request: TextRequest,
        model: str,
    ) -> AsyncIterator[str]:
        """
        Stream text generation from a specific model.

        Args:
            request: Text request with prompt, messages, etc.
            model: Model string in "provider/model" format

        Yields:
            Text content chunks as they arrive

        Raises:
            ValueError: If model string is invalid
            ProviderError: If provider call fails
        """
        provider, model_name = self._parse_model_string(model)
        adapter = self.registry.get_for_model(model)

        add_info(
            layer=SDKLayer.CLIENT.value,
            action="text_stream_start",
            message=f"Starting text stream with {provider}/{model_name}",
            provider=provider,
            model=model_name,
        )

        # Build kwargs from request
        kwargs: Dict[str, Any] = {}
        if request.temperature is not None:
            kwargs["temperature"] = request.temperature
        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens
        if request.top_p is not None:
            kwargs["top_p"] = request.top_p
        if request.stop is not None:
            kwargs["stop"] = request.stop
        if request.response_format is not None:
            kwargs["response_format"] = request.response_format
        if request.tools is not None:
            kwargs["tools"] = request.tools
        if request.tool_choice is not None:
            kwargs["tool_choice"] = request.tool_choice
        if request.provider_params:
            kwargs.update(request.provider_params)

        # Convert prompt to messages if needed
        messages = request.messages
        if messages is None and request.prompt:
            messages = [{"role": "user", "content": request.prompt}]
            if request.system:
                messages.insert(0, {"role": "system", "content": request.system})

        if not messages:
            raise ValueError("Either 'messages' or 'prompt' must be provided")

        async for chunk in adapter.complete_stream(
            messages=messages,
            model=model_name,
            **kwargs,
        ):
            yield chunk


__all__ = ["UnifiedTextClient"]
