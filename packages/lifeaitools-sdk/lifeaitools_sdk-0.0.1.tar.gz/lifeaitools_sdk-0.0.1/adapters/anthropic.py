"""Anthropic adapter for Unified AI SDK - Text/LLM capability only."""

import time
from typing import Any, AsyncIterator, Dict, List, Optional, Set

from ..breadcrumbs import add_info, SDKLayer
from ..config import ProviderConfig
from ..configs.loader import get_provider_config
from ..exceptions import ProviderError
from ..models import Capability
from ..models.usage import TokenUsage, UsageBreadcrumb
from ..utils.cost_calculator import get_cost_calculator
from .base import BaseAdapter


class AnthropicAdapter(BaseAdapter):
    """
    Anthropic adapter with text completion support.

    Capabilities:
        - TEXT: Chat completions with Claude models

    Note:
        Anthropic does NOT provide TTS or STT capabilities via API.
        Voice features in Claude app use third-party providers (ElevenLabs).
        Use OpenAI, ElevenLabs, or Gemini adapters for audio capabilities.

    Models:
        - claude-opus-4-5-20251101 (latest, highest capability)
        - claude-sonnet-4-20250514 (balanced)
        - claude-3-5-haiku-20241022 (fast, affordable)
    """

    name = "anthropic"

    # Default models
    DEFAULT_MODELS = {
        "text": "claude-sonnet-4-20250514",
    }

    def __init__(self, api_key: str, config: Optional[ProviderConfig] = None) -> None:
        super().__init__(api_key, config)
        self._client = None

    @property
    def capabilities(self) -> Set[Capability]:
        return {Capability.TEXT}

    def _init_client(self) -> Any:
        """Initialize Anthropic client."""
        try:
            from anthropic import Anthropic
            return Anthropic(api_key=self.api_key)
        except ImportError:
            raise ImportError("anthropic package required: pip install anthropic")

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
        Generate text with Claude.

        Args:
            messages: Chat messages in OpenAI format (converted internally)
            model: Claude model ID
            **kwargs: Additional parameters:
                - temperature: 0.0 to 1.0
                - max_tokens: Maximum response tokens (required, default 4096)
                - top_p: Nucleus sampling parameter
                - stop_sequences: List of stop strings
                - system: System prompt (extracted from messages if present)
                - response_format: {"type": "json_object"} for JSON mode

        Returns:
            Dict with completion result
        """
        model = model or self.DEFAULT_MODELS["text"]
        self._breadcrumb_call_start("complete", model, message_count=len(messages))
        start_time = time.time()

        try:
            # Extract system message if present
            system_prompt = kwargs.get("system", "")
            filtered_messages = []

            for msg in messages:
                if msg.get("role") == "system":
                    system_prompt = msg.get("content", "")
                else:
                    # Anthropic uses 'user' and 'assistant' roles
                    filtered_messages.append({
                        "role": msg.get("role"),
                        "content": msg.get("content"),
                    })

            # Build API kwargs
            # NOTE: Anthropic API REQUIRES max_tokens
            api_kwargs: Dict[str, Any] = {
                "model": model,
                "messages": filtered_messages,
            }

            # max_tokens is required by Anthropic
            # Use provided value OR model's max_output_tokens from config
            if kwargs.get("max_tokens") is not None:
                api_kwargs["max_tokens"] = kwargs["max_tokens"]
            else:
                # Get model-specific max from config
                model_config = get_provider_config().get_model_config("anthropic", "text", model)
                max_output = model_config.get("max_output_tokens")
                if max_output:
                    api_kwargs["max_tokens"] = max_output
                # If not in config, let Anthropic API return clear error

            if system_prompt:
                api_kwargs["system"] = system_prompt
            if kwargs.get("temperature") is not None:
                api_kwargs["temperature"] = kwargs["temperature"]
            if kwargs.get("top_p") is not None:
                api_kwargs["top_p"] = kwargs["top_p"]
            if kwargs.get("stop_sequences") or kwargs.get("stop"):
                api_kwargs["stop_sequences"] = kwargs.get("stop_sequences") or kwargs.get("stop")

            response = self.client.messages.create(**api_kwargs)

            # Extract content
            content = ""
            for block in response.content:
                if block.type == "text":
                    content += block.text

            latency_ms = (time.time() - start_time) * 1000

            # Parse usage and calculate cost
            raw_usage = {
                "input_tokens": response.usage.input_tokens if response.usage else 0,
                "output_tokens": response.usage.output_tokens if response.usage else 0,
                "cache_creation_input_tokens": getattr(response.usage, "cache_creation_input_tokens", 0) if response.usage else 0,
                "cache_read_input_tokens": getattr(response.usage, "cache_read_input_tokens", 0) if response.usage else 0,
            }
            usage = TokenUsage.from_anthropic(raw_usage)
            cost = get_cost_calculator().calculate_llm_cost("anthropic", model, usage)

            # Add usage breadcrumb
            usage_bc = UsageBreadcrumb(
                provider="anthropic",
                model=model,
                service="text",
                tokens=usage,
                cost=cost,
                provider_usage=raw_usage,
            )
            add_info(
                layer=SDKLayer.ADAPTER.value,
                action="api_usage",
                message=f"Anthropic: {usage.total_tokens} tokens, ${cost.total_cost:.6f}",
                **usage_bc.to_breadcrumb_dict(),
            )

            self._breadcrumb_call_success("complete", model, {
                "latency_ms": latency_ms,
                "content_length": len(content),
                "stop_reason": response.stop_reason,
                "tokens": usage.total_tokens,
            })

            return {
                "content": content,
                "finish_reason": response.stop_reason,
                "usage": {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                }
            }

        except Exception as e:
            self._breadcrumb_call_error("complete", model, e)
            raise ProviderError(f"Anthropic completion failed: {e}", self.name, model)

    async def complete_stream(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """
        Stream text completion from Claude.

        Args:
            messages: Chat messages in OpenAI format (converted internally)
            model: Claude model ID
            **kwargs: Additional parameters:
                - max_tokens: Maximum response tokens (required, default 4096)
                - temperature: 0.0 to 1.0
                - system: System prompt (extracted from messages if present)

        Yields:
            Text chunks as they are generated
        """
        model = model or self.DEFAULT_MODELS["text"]
        self._breadcrumb_call_start("complete_stream", model, message_count=len(messages))

        try:
            # Extract system message if present
            system_prompt = kwargs.get("system", "")
            filtered_messages = []

            for msg in messages:
                if msg.get("role") == "system":
                    system_prompt = msg.get("content", "")
                else:
                    filtered_messages.append({
                        "role": msg.get("role"),
                        "content": msg.get("content"),
                    })

            # Build API kwargs
            # NOTE: Anthropic API REQUIRES max_tokens
            api_kwargs: Dict[str, Any] = {
                "model": model,
                "messages": filtered_messages,
            }

            # max_tokens is required by Anthropic
            # Use provided value OR model's max_output_tokens from config
            if kwargs.get("max_tokens") is not None:
                api_kwargs["max_tokens"] = kwargs["max_tokens"]
            else:
                # Get model-specific max from config
                model_config = get_provider_config().get_model_config("anthropic", "text", model)
                max_output = model_config.get("max_output_tokens")
                if max_output:
                    api_kwargs["max_tokens"] = max_output
                # If not in config, let Anthropic API return clear error

            if system_prompt:
                api_kwargs["system"] = system_prompt
            if kwargs.get("temperature") is not None:
                api_kwargs["temperature"] = kwargs["temperature"]

            with self.client.messages.stream(**api_kwargs) as stream:
                for text in stream.text_stream:
                    yield text

        except Exception as e:
            self._breadcrumb_call_error("complete_stream", model, e)
            raise ProviderError(f"Anthropic streaming failed: {e}", self.name, model)

    async def health_check(self) -> bool:
        """Test connectivity to Anthropic API."""
        try:
            # Simple test - just try to create client
            _ = self.client
            return True
        except Exception:
            return False


__all__ = ["AnthropicAdapter"]
