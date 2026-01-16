"""
Unified TTS Client for Unified AI SDK.

Provides text-to-speech capabilities with:
- Multi-provider support (ElevenLabs, Gemini, etc.)
- Fallback chain with breadcrumb tracking
- Streaming support
- Voice listing across providers
"""

import time
from typing import Any, AsyncIterator, Dict, List, Optional

from ..breadcrumbs import (
    add_error,
    add_info,
    add_success,
    add_warning,
    get_collector,
    SDKLayer,
)
from ..exceptions import AllProvidersFailedError, ProviderError
from ..models import (
    AudioFormat,
    RawAudioResponse,
    TTSRequest,
    TTSResponse,
    VoiceInfo,
)
from .base import AdapterRegistry, BaseCapabilityClient


class UnifiedTTSClient(BaseCapabilityClient[TTSRequest, TTSResponse]):
    """
    Unified TTS client with multi-provider fallback support.

    Features:
        - Execute TTS on specific provider/model
        - Automatic fallback through provider chain
        - Full breadcrumb tracking for debugging
        - Streaming TTS support
        - Voice listing across all providers

    Example:
        registry = AdapterRegistry()
        registry.register(ElevenLabsAdapter(api_key="xi-..."))
        registry.register(GeminiAdapter(api_key="..."))

        client = UnifiedTTSClient(
            registry=registry,
            fallback_chain=[
                "elevenlabs/eleven_multilingual_v2",
                "gemini/gemini-2.0-flash",
            ]
        )

        request = TTSRequest(text="Hello world", voice="Rachel")
        response = await client.execute_with_fallback(request)
    """

    CAPABILITY: str = "tts"

    async def execute(self, request: TTSRequest, model: str) -> TTSResponse:
        """
        Execute TTS on a specific model.

        Args:
            request: TTS request with text, voice, format settings
            model: Model string in "provider/model" format
                   e.g., "elevenlabs/eleven_multilingual_v2"

        Returns:
            TTSResponse with audio data and metadata

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
            action="tts_execute_start",
            message=f"Executing TTS with {provider}/{model_name}",
            provider=provider,
            model=model_name,
            text_length=len(request.text),
            voice=request.voice,
        )

        kwargs: Dict[str, Any] = {}
        if request.output_format:
            kwargs["output_format"] = self._format_to_elevenlabs(request.output_format)
        if request.provider_params:
            kwargs.update(request.provider_params)

        raw_audio: RawAudioResponse = await adapter.tts(
            text=request.text,
            model=model_name,
            voice=request.voice,
            **kwargs,
        )

        latency_ms = (time.time() - start_time) * 1000

        response = TTSResponse(
            success=True,
            provider=provider,
            model=model_name,
            latency_ms=latency_ms,
            audio=raw_audio,
            text_length=len(request.text),
            voice_used=request.voice,
            format_requested=request.output_format,
            format_actual=raw_audio.format,
            metadata={
                "audio_bytes": len(raw_audio.data),
                "sample_rate": raw_audio.sample_rate,
                "channels": raw_audio.channels,
            },
        )

        return response

    async def execute_with_fallback(self, request: TTSRequest) -> TTSResponse:
        """
        Execute TTS with fallback chain - full breadcrumb tracking.

        Tries each provider in the fallback chain until one succeeds.
        Records breadcrumbs at each step for debugging.

        Args:
            request: TTS request with text, voice, format settings

        Returns:
            TTSResponse from first successful provider

        Raises:
            AllProvidersFailedError: If all providers in chain fail
        """
        add_info(
            layer=SDKLayer.CLIENT.value,
            action="fallback_chain_start",
            message=f"Starting TTS with fallback chain: {self.fallback_chain}",
            capability="tts",
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
                    action="tts_complete",
                    message=f"TTS completed with {provider}",
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
                message="All TTS providers failed",
                failed_providers=failed_providers,
            ),
            recommendations=[
                "Check all provider API keys",
                "Verify network connectivity",
                "Review provider status pages",
            ],
            failed_providers=failed_providers,
        )

        collector = get_collector()
        raise AllProvidersFailedError(
            message="All TTS providers failed",
            failed_providers=failed_providers,
            breadcrumbs=collector.get_all() if collector else [],
        )

    async def stream(
        self,
        request: TTSRequest,
        model: str,
    ) -> AsyncIterator[bytes]:
        """
        Stream TTS audio chunks from a specific model.

        Args:
            request: TTS request with text, voice settings
            model: Model string in "provider/model" format

        Yields:
            Audio data chunks as they arrive

        Raises:
            ValueError: If model string is invalid
            ProviderError: If provider call fails
        """
        provider, model_name = self._parse_model_string(model)
        adapter = self.registry.get_for_model(model)

        add_info(
            layer=SDKLayer.CLIENT.value,
            action="tts_stream_start",
            message=f"Starting TTS stream with {provider}/{model_name}",
            provider=provider,
            model=model_name,
            text_length=len(request.text),
            voice=request.voice,
        )

        kwargs: Dict[str, Any] = {}
        if request.output_format:
            kwargs["output_format"] = self._format_to_elevenlabs(request.output_format)
        if request.provider_params:
            kwargs.update(request.provider_params)

        async for chunk in adapter.tts_stream(
            text=request.text,
            model=model_name,
            voice=request.voice,
            **kwargs,
        ):
            yield chunk

    async def get_available_voices(
        self,
        provider: Optional[str] = None,
    ) -> Dict[str, List[VoiceInfo]]:
        """
        Get available voices from all or specific provider.

        Args:
            provider: Optional provider name to filter by.
                     If None, returns voices from all providers.

        Returns:
            Dict mapping provider names to their voice lists

        Example:
            voices = await client.get_available_voices()
            # {"elevenlabs": [VoiceInfo(...), ...], "gemini": [...]}

            voices = await client.get_available_voices("elevenlabs")
            # {"elevenlabs": [VoiceInfo(...), ...]}
        """
        result: Dict[str, List[VoiceInfo]] = {}

        providers_to_check = (
            [provider] if provider else self.registry.list_providers()
        )

        for prov_name in providers_to_check:
            adapter = self.registry.get(prov_name)
            if adapter is None:
                continue

            if hasattr(adapter, "get_voices"):
                try:
                    voices = await adapter.get_voices()
                    result[prov_name] = voices
                except Exception as e:
                    add_warning(
                        layer=SDKLayer.CLIENT.value,
                        action="get_voices_failed",
                        message=f"Failed to get voices from {prov_name}: {e}",
                        provider=prov_name,
                        error=str(e),
                    )
                    result[prov_name] = []

        return result

    def _format_to_elevenlabs(self, fmt: AudioFormat) -> str:
        """
        Convert AudioFormat enum to ElevenLabs format string.

        Args:
            fmt: AudioFormat enum value

        Returns:
            ElevenLabs format string (e.g., "mp3_44100_128")
        """
        format_map = {
            AudioFormat.MP3: "mp3_44100_128",
            AudioFormat.WAV: "pcm_44100",
            AudioFormat.PCM: "pcm_44100",
            AudioFormat.OGG: "ogg_44100_64",
            AudioFormat.OPUS: "opus_44100_64",
        }
        return format_map.get(fmt, "mp3_44100_128")


__all__ = ["UnifiedTTSClient"]
