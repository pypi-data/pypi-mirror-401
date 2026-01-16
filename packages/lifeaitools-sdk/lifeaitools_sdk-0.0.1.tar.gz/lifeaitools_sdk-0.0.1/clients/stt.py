"""
Unified STT Client for Unified AI SDK.

Provides speech-to-text transcription capabilities with:
- Multi-provider support (ElevenLabs, OpenAI)
- Fallback chain with breadcrumb tracking
- Support for various audio formats
"""

import time
from typing import Any, Dict, List, Union

from ..breadcrumbs import add_error, add_info, add_success, add_warning, SDKLayer
from ..exceptions import AllProvidersFailedError, ProviderError
from ..models import STTRequest, STTResponse
from .base import AdapterRegistry, BaseCapabilityClient


class UnifiedSTTClient(BaseCapabilityClient[STTRequest, STTResponse]):
    """
    Unified STT client with multi-provider fallback support.

    Features:
        - Execute STT on specific provider/model
        - Automatic fallback through provider chain
        - Full breadcrumb tracking for debugging

    Example:
        registry = AdapterRegistry()
        registry.register(ElevenLabsAdapter(api_key="xi-..."))
        registry.register(OpenAIAdapter(api_key="sk-..."))

        client = UnifiedSTTClient(
            registry=registry,
            fallback_chain=[
                "elevenlabs/scribe_v1",
                "openai/whisper-1",
            ]
        )

        request = STTRequest(audio=audio_bytes, language="en")
        response = await client.execute_with_fallback(request)
    """

    CAPABILITY: str = "stt"

    async def execute(self, request: STTRequest, model: str) -> STTResponse:
        """
        Execute STT on a specific model.

        Args:
            request: STT request with audio data and settings
            model: Model string in "provider/model" format
                   e.g., "elevenlabs/scribe_v1"

        Returns:
            STTResponse with transcription and metadata

        Raises:
            ValueError: If model string is invalid
            ProviderError: If provider call fails
            RateLimitError: If rate limited
            QuotaExceededError: If quota exhausted
        """
        start_time = time.time()
        provider, model_name = self._parse_model_string(model)

        adapter = self.registry.get_for_model(model)

        add_info(
            layer=SDKLayer.CLIENT.value,
            action="stt_execute_start",
            message=f"Executing STT with {provider}/{model_name}",
            provider=provider,
            model=model_name,
            has_audio=bool(request.audio),
            language=request.language,
        )

        # Prepare audio data
        audio_data: bytes
        if isinstance(request.audio, str):
            with open(request.audio, "rb") as f:
                audio_data = f.read()
        else:
            audio_data = request.audio

        # Build kwargs from request
        kwargs: Dict[str, Any] = {}
        if request.language is not None:
            kwargs["language"] = request.language
        if request.response_format is not None:
            kwargs["response_format"] = request.response_format
        if request.timestamp_granularity is not None:
            kwargs["timestamp_granularity"] = request.timestamp_granularity
        if request.provider_params:
            kwargs.update(request.provider_params)

        result = await adapter.transcribe(
            audio=audio_data,
            model=model_name,
            **kwargs,
        )

        latency_ms = (time.time() - start_time) * 1000

        add_success(
            layer=SDKLayer.CLIENT.value,
            action="stt_execute_complete",
            message=f"STT completed with {provider}/{model_name}",
            provider=provider,
            model=model_name,
            latency_ms=latency_ms,
            text_length=len(result.get("text", "")),
        )

        return STTResponse(
            success=True,
            provider=provider,
            model=model_name,
            latency_ms=latency_ms,
            text=result.get("text", ""),
            language=result.get("language"),
            duration_seconds=result.get("duration"),
            segments=result.get("segments", []),
            words=result.get("words"),
            usage=result.get("usage", {}),
        )

    async def execute_with_fallback(self, request: STTRequest) -> STTResponse:
        """
        Execute STT with fallback chain - full breadcrumb tracking.

        Tries each provider in the fallback chain until one succeeds.
        Records breadcrumbs at each step for debugging.

        Args:
            request: STT request with audio data and settings

        Returns:
            STTResponse from first successful provider

        Raises:
            AllProvidersFailedError: If all providers in chain fail
        """
        add_info(
            layer=SDKLayer.CLIENT.value,
            action="fallback_chain_start",
            message=f"Starting STT with fallback chain: {self.fallback_chain}",
            capability="stt",
            chain=self.fallback_chain,
        )

        failed_providers: List[Dict[str, Any]] = []

        for i, model in enumerate(self.fallback_chain):
            provider = model.split("/")[0]

            add_info(
                layer=SDKLayer.CLIENT.value,
                action="provider_attempt",
                message=f"Attempting provider {i + 1}/{len(self.fallback_chain)}: {provider}",
                provider=provider,
                model=model,
                attempt=i + 1,
            )

            try:
                result = await self.execute(request, model)

                add_success(
                    layer=SDKLayer.CLIENT.value,
                    action="stt_complete",
                    message=f"STT completed with {provider}",
                    provider=provider,
                    model=model,
                    fallback_used=i > 0,
                    attempts=i + 1,
                )

                return result

            except Exception as e:
                failed_providers.append({
                    "provider": provider,
                    "model": model,
                    "error": str(e),
                    "error_type": type(e).__name__,
                })

                if i < len(self.fallback_chain) - 1:
                    next_provider = self.fallback_chain[i + 1].split("/")[0]
                    add_warning(
                        layer=SDKLayer.FALLBACK.value,
                        action="fallback_triggered",
                        message=f"{provider} failed, falling back to next provider",
                        failed_provider=provider,
                        error=str(e),
                        next_provider=next_provider,
                    )
                continue

        add_error(
            layer=SDKLayer.CLIENT.value,
            action="all_providers_failed",
            error=AllProvidersFailedError(
                message="All STT providers failed",
                failed_providers=failed_providers,
            ),
            recommendations=[
                "Check all provider API keys",
                "Verify audio format compatibility",
                "Review provider status pages",
            ],
            failed_providers=failed_providers,
        )

        raise AllProvidersFailedError(
            message="All STT providers failed",
            failed_providers=failed_providers,
        )


__all__ = ["UnifiedSTTClient"]
