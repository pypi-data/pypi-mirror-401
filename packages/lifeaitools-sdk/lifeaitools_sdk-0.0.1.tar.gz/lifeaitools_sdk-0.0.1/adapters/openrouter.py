"""OpenRouter adapter for Unified AI SDK - Text/LLM capability via multi-model gateway."""

import time
from typing import Any, AsyncIterator, Dict, List, Optional, Set

from ..breadcrumbs import add_info, SDKLayer
from ..config import ProviderConfig
from ..exceptions import ProviderError
from ..models import Capability
from ..models.usage import TokenUsage, UsageBreadcrumb
from ..utils.cost_calculator import get_cost_calculator
from .base import BaseAdapter


class OpenRouterAdapter(BaseAdapter):
    """
    OpenRouter adapter for unified access to 400+ LLM models.

    Capabilities:
        - TEXT: Chat completions via OpenAI-compatible API

    Note:
        OpenRouter is a gateway that routes to many providers (OpenAI, Anthropic,
        Google, Mistral, etc.) with a unified API. No TTS/STT capabilities.

    Features:
        - Access to 400+ models with one API key
        - Automatic fallback routing
        - Pass-through pricing (no markup)
        - Zero data retention option

    Model Format:
        - Use full model ID: "anthropic/claude-sonnet-4"
        - Shortcuts: ":nitro" for fast, ":floor" for cheap

    Popular Models (2025):
        - anthropic/claude-sonnet-4.5 (Claude latest)
        - openai/gpt-4o (GPT-4 latest)
        - google/gemini-2.5-flash (Gemini latest)
        - deepseek/deepseek-v3 (Open-source leader)
    """

    name = "openrouter"

    # OpenRouter API endpoint
    API_BASE = "https://openrouter.ai/api/v1"

    # Default models
    DEFAULT_MODELS = {
        "text": "anthropic/claude-sonnet-4",
    }

    def __init__(self, api_key: str, config: Optional[ProviderConfig] = None) -> None:
        super().__init__(api_key, config)
        self._client = None

    @property
    def capabilities(self) -> Set[Capability]:
        return {Capability.TEXT}

    def _init_client(self) -> Any:
        """Initialize OpenAI-compatible client pointing to OpenRouter."""
        try:
            from openai import OpenAI
            return OpenAI(
                base_url=self.API_BASE,
                api_key=self.api_key,
                default_headers={
                    "HTTP-Referer": "https://unified-ai-sdk.local",
                    "X-Title": "Unified AI SDK",
                }
            )
        except ImportError:
            raise ImportError("openai package required: pip install openai")

    @property
    def client(self):
        if self._client is None:
            self._client = self._init_client()
        return self._client

    async def complete(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate text via OpenRouter.

        Args:
            messages: Chat messages in OpenAI format
            model: Full model ID (e.g., "anthropic/claude-sonnet-4")
            **kwargs: Additional parameters:
                - temperature: 0.0 to 2.0 (model-dependent)
                - max_tokens: Maximum response tokens
                - top_p: Nucleus sampling parameter
                - stop: List of stop strings
                - response_format: {"type": "json_object"} for JSON mode
                - provider: Specific provider preferences
                - route: Routing strategy ("fallback", etc.)

        Returns:
            Dict with completion result
        """
        model = model or self.DEFAULT_MODELS["text"]
        self._breadcrumb_call_start("complete", model, message_count=len(messages))
        start_time = time.time()

        try:
            api_kwargs: Dict[str, Any] = {
                "model": model,
                "messages": messages,
            }

            if kwargs.get("temperature") is not None:
                api_kwargs["temperature"] = kwargs["temperature"]
            if kwargs.get("max_tokens") is not None:
                api_kwargs["max_tokens"] = kwargs["max_tokens"]
            if kwargs.get("top_p") is not None:
                api_kwargs["top_p"] = kwargs["top_p"]
            if kwargs.get("stop") is not None:
                api_kwargs["stop"] = kwargs["stop"]
            if kwargs.get("response_format") is not None:
                api_kwargs["response_format"] = kwargs["response_format"]

            # OpenRouter-specific parameters
            extra_body = {}
            if kwargs.get("provider"):
                extra_body["provider"] = kwargs["provider"]
            if kwargs.get("route"):
                extra_body["route"] = kwargs["route"]
            if extra_body:
                api_kwargs["extra_body"] = extra_body

            response = self.client.chat.completions.create(**api_kwargs)

            content = response.choices[0].message.content or ""
            finish_reason = response.choices[0].finish_reason

            latency_ms = (time.time() - start_time) * 1000

            # Parse usage (OpenAI format)
            raw_usage = {
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            }
            usage = TokenUsage.from_openai(raw_usage)
            cost = get_cost_calculator().calculate_llm_cost("openrouter", model, usage)

            # Add usage breadcrumb
            usage_bc = UsageBreadcrumb(
                provider="openrouter",
                model=model,
                service="text",
                tokens=usage,
                cost=cost,
                provider_usage=raw_usage,
            )
            add_info(
                layer=SDKLayer.ADAPTER.value,
                action="api_usage",
                message=f"OpenRouter ({model}): {usage.total_tokens} tokens, ${cost.total_cost:.6f}",
                **usage_bc.to_breadcrumb_dict(),
            )

            self._breadcrumb_call_success("complete", model, {
                "latency_ms": latency_ms,
                "content_length": len(content),
                "finish_reason": finish_reason,
                "tokens": usage.total_tokens,
            })

            return {
                "content": content,
                "finish_reason": finish_reason,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                }
            }

        except Exception as e:
            self._breadcrumb_call_error("complete", model, e)
            raise ProviderError(f"OpenRouter completion failed: {e}", self.name, model)

    async def complete_stream(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """
        Stream text completion via OpenRouter.

        Args:
            messages: Chat messages in OpenAI format
            model: Full model ID (e.g., "anthropic/claude-sonnet-4")
            **kwargs: Additional parameters

        Yields:
            Text chunks as they are generated
        """
        model = model or self.DEFAULT_MODELS["text"]
        self._breadcrumb_call_start("complete_stream", model, message_count=len(messages))

        try:
            api_kwargs: Dict[str, Any] = {
                "model": model,
                "messages": messages,
                "stream": True,
            }

            if kwargs.get("temperature") is not None:
                api_kwargs["temperature"] = kwargs["temperature"]
            if kwargs.get("max_tokens") is not None:
                api_kwargs["max_tokens"] = kwargs["max_tokens"]

            # OpenRouter-specific parameters
            extra_body = {}
            if kwargs.get("provider"):
                extra_body["provider"] = kwargs["provider"]
            if extra_body:
                api_kwargs["extra_body"] = extra_body

            stream = self.client.chat.completions.create(**api_kwargs)

            for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            self._breadcrumb_call_error("complete_stream", model, e)
            raise ProviderError(f"OpenRouter streaming failed: {e}", self.name, model)

    async def list_models(self) -> List[Dict[str, Any]]:
        """
        Get list of available models from OpenRouter.

        Returns:
            List of model info dicts with id, name, pricing, context_length, etc.
        """
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.API_BASE}/models",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("data", [])
                    else:
                        return []
        except Exception:
            return []

    async def health_check(self) -> bool:
        """Test connectivity to OpenRouter API."""
        try:
            models = await self.list_models()
            return len(models) > 0
        except Exception:
            return False

    async def close(self) -> None:
        """Close the adapter and release resources."""
        self._client = None


__all__ = ["OpenRouterAdapter"]
