"""
UnifiedAI SDK Entry Point.

Main SDK class that provides a unified interface for AI capabilities
with automatic breadcrumb collection and multi-provider fallback support.

Example:
    # From environment variables
    sdk = UnifiedAI.from_env()

    # Or with explicit config
    config = Config(
        providers={
            "elevenlabs": ProviderConfig(api_key="xi-..."),
            "gemini": ProviderConfig(api_key="..."),
        },
        defaults={"tts": "elevenlabs/eleven_multilingual_v2"},
    )
    sdk = UnifiedAI(config)

    # Generate speech
    response = await sdk.generate_speech("Hello world", voice="Rachel")
    response.save("output.mp3")
"""

import uuid
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

from .adapters import BaseAdapter, ElevenLabsAdapter, GeminiAdapter
from .breadcrumbs import add_info, get_collector, SDKLayer, start_collection

if TYPE_CHECKING:
    from .presets import TTSPreset
from .clients import AdapterRegistry, UnifiedTTSClient, UnifiedTextClient
from .config import Config
from .exceptions import ConfigurationError
from .models import AudioFormat, TTSRequest, TTSResponse, TextRequest, TextResponse, VoiceInfo
from .breadcrumbs import add_error


class UnifiedAI:
    """
    Main SDK entry point with automatic breadcrumb collection.

    Provides a unified interface for AI capabilities (TTS, STT, Text, etc.)
    with multi-provider support, automatic fallback, and full observability
    through breadcrumb tracking.

    Attributes:
        config: SDK configuration with providers, defaults, and fallback chains
        tts: TTS capability client for direct access

    Example:
        sdk = UnifiedAI.from_env()

        # High-level API with automatic breadcrumb collection
        response = await sdk.generate_speech(
            text="Hello world",
            voice="Rachel",
            output_format=AudioFormat.MP3,
        )
        print(f"Audio: {len(response.audio.data)} bytes")
        print(f"Breadcrumbs: {len(response.breadcrumbs)} entries")

        # Or use direct client access
        request = TTSRequest(text="Hello", voice="Rachel")
        response = await sdk.tts.execute_with_fallback(request)
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize UnifiedAI SDK with configuration.

        Args:
            config: SDK configuration with providers, fallbacks, and defaults
        """
        self.config = config
        self._registry = AdapterRegistry()
        self._tts_client: Optional[UnifiedTTSClient] = None
        self._text_client: Optional[UnifiedTextClient] = None
        self._setup_adapters()
        self._setup_clients()

    def _setup_adapters(self) -> None:
        """
        Initialize and register adapters based on config.

        Creates adapter instances for each enabled provider in config
        and registers them with the adapter registry.
        """
        # Map of provider names to adapter classes
        adapter_classes: Dict[str, type] = {
            "elevenlabs": ElevenLabsAdapter,
            "gemini": GeminiAdapter,
            # Future: "openai": OpenAIAdapter, "anthropic": AnthropicAdapter
        }

        for provider_name, provider_config in self.config.providers.items():
            if not provider_config.enabled:
                continue

            adapter_class = adapter_classes.get(provider_name)
            if adapter_class is None:
                # Skip providers without implemented adapters
                continue

            try:
                adapter = adapter_class(
                    api_key=provider_config.api_key,
                    config=provider_config,
                )
                self._registry.register(adapter)
            except Exception:
                # Skip adapters that fail to initialize (e.g., missing optional dependencies)
                pass

    def _setup_clients(self) -> None:
        """
        Initialize capability clients.

        Creates client instances for each capability with their respective
        fallback chains from configuration.
        """
        available_providers = set(self._registry.list_providers())

        # Setup TTS client
        tts_fallback = self.config.get_fallback_chain("tts")
        filtered_tts_fallback = [
            model for model in tts_fallback
            if model.split("/")[0] in available_providers
        ]

        if filtered_tts_fallback or available_providers:
            self._tts_client = UnifiedTTSClient(
                registry=self._registry,
                fallback_chain=filtered_tts_fallback,
            )

        # Setup Text client
        text_fallback = self.config.get_fallback_chain("text")
        filtered_text_fallback = [
            model for model in text_fallback
            if model.split("/")[0] in available_providers
        ]

        if filtered_text_fallback or available_providers:
            self._text_client = UnifiedTextClient(
                registry=self._registry,
                fallback_chain=filtered_text_fallback,
            )

    @property
    def tts(self) -> UnifiedTTSClient:
        """
        TTS capability client for direct access.

        Returns:
            UnifiedTTSClient instance

        Raises:
            ConfigurationError: If TTS is not configured (no providers available)
        """
        if self._tts_client is None:
            raise ConfigurationError(
                message="TTS not configured - no TTS providers available",
                recommendations=[
                    "Add ElevenLabs API key via ELEVENLABS_API_KEY env var",
                    "Add Gemini API key via GOOGLE_API_KEY env var",
                    "Ensure at least one TTS provider is configured",
                ],
            )
        return self._tts_client

    @property
    def text_client(self) -> UnifiedTextClient:
        """
        Text/LLM capability client for direct access.

        Returns:
            UnifiedTextClient instance

        Raises:
            ConfigurationError: If Text is not configured (no providers available)
        """
        if self._text_client is None:
            raise ConfigurationError(
                message="Text/LLM not configured - no text providers available",
                recommendations=[
                    "Add Gemini API key via GEMINI_API_KEY env var",
                    "Add OpenAI API key via OPENAI_API_KEY env var",
                    "Ensure at least one LLM provider is configured",
                ],
            )
        return self._text_client

    async def generate_speech(
        self,
        text: str,
        voice: Optional[str] = None,
        model: Optional[str] = None,
        output_format: Optional[Union[AudioFormat, str]] = None,
        preset: Optional[Union[str, "TTSPreset"]] = None,
        include_breadcrumbs: bool = True,
        **kwargs: Any,
    ) -> TTSResponse:
        """
        High-level TTS API with automatic breadcrumb collection.

        Args:
            text: Text to convert (may include SSML breaks from LLM)
            voice: Voice name. Overrides preset if provided.
            model: Model "provider/model" format. Overrides preset.
            output_format: Audio format (mp3/wav/ogg). Overrides preset.
            preset: Preset name like "gemini/warm_trainer" or TTSPreset.
            include_breadcrumbs: Include breadcrumbs in response
            **kwargs: provider_params dict with temperature, streaming, etc.

        Returns:
            TTSResponse with audio data, metadata, breadcrumbs

        Example:
            # With preset (production)
            response = await sdk.generate_speech(text, preset="gemini/warm_trainer")

            # Or explicit params
            response = await sdk.generate_speech(
                text, voice="Enceladus",
                provider_params={"temperature": 1.35, "streaming": True}
            )
        """
        # Start breadcrumb collection
        request_id = str(uuid.uuid4())
        collector = start_collection(request_id)

        # Load preset if provided
        preset_obj = None
        if preset:
            from .presets import load_preset, TTSPreset
            if isinstance(preset, str):
                preset_obj = load_preset(preset)
            else:
                preset_obj = preset

        # Apply preset defaults, explicit params override
        if preset_obj:
            effective_voice = voice or preset_obj.voice
            effective_model = model or preset_obj.model_string
            effective_format = output_format or preset_obj.output_format
            # Merge provider_params: preset first, then kwargs override
            base_params = preset_obj.to_kwargs().get("provider_params", {})
            base_params.update(kwargs.get("provider_params", {}))
            effective_provider_params = base_params
        else:
            effective_voice = voice or "default"
            effective_model = model or self.config.defaults.get("tts")
            effective_format = output_format or AudioFormat.MP3
            effective_provider_params = kwargs.get("provider_params", {})

        # Normalize output_format to AudioFormat enum
        if isinstance(effective_format, str):
            effective_format = AudioFormat(effective_format)

        add_info(
            layer=SDKLayer.SDK.value,
            action="tts_request_received",
            message="TTS request received",
            request_id=request_id,
            text_length=len(text),
            model=effective_model,
            voice=effective_voice,
            output_format=effective_format.value,
            preset=preset if isinstance(preset, str) else None,
        )

        try:
            # Build request
            request = TTSRequest(
                text=text,
                voice=effective_voice,
                model=effective_model,
                output_format=effective_format,
                speed=kwargs.get("speed", 1.0),
                pitch=kwargs.get("pitch", 1.0),
                language=kwargs.get("language"),
                provider_params=effective_provider_params,
            )

            # Execute with appropriate method
            if effective_model:
                result = await self.tts.execute(request, effective_model)
            else:
                result = await self.tts.execute_with_fallback(request)

            # Add breadcrumbs to response
            if include_breadcrumbs:
                result.breadcrumbs = collector.get_all()
                result.execution_warnings = collector.get_warnings()

            return result

        except Exception as e:
            # Ensure breadcrumbs are attached to exception
            if hasattr(e, "breadcrumbs"):
                e.breadcrumbs = collector.get_all()
            raise

    async def text(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, Any]]] = None,
        model: Optional[str] = None,
        system: Optional[str] = None,
        response_format: Optional[Dict[str, Any]] = None,
        include_breadcrumbs: bool = True,
        **kwargs: Any,
    ) -> TextResponse:
        """
        High-level LLM API with automatic breadcrumb collection.

        Args:
            prompt: Simple text prompt (converted to messages)
            messages: Chat messages in OpenAI format
            model: Model "provider/model" format (e.g., "gemini/gemini-2.0-flash")
            system: System prompt
            response_format: {"type": "json_object"} for JSON mode
            include_breadcrumbs: Include breadcrumbs in response
            **kwargs: temperature, max_tokens, top_p, stop, provider_params

        Returns:
            TextResponse with content and metadata

        Example:
            # Simple prompt
            response = await sdk.text("What is 2+2?")

            # JSON mode
            response = await sdk.text(
                prompt="Extract: John Smith, age 30",
                response_format={"type": "json_object"},
                system="Return JSON: {name, age}"
            )
        """
        request_id = str(uuid.uuid4())
        collector = start_collection(request_id)

        effective_model = model or self.config.defaults.get("text")

        add_info(
            layer=SDKLayer.SDK.value,
            action="text_request_received",
            message="Text/LLM request received",
            request_id=request_id,
            model=effective_model,
            has_json_mode=response_format is not None,
        )

        try:
            request = TextRequest(
                prompt=prompt,
                messages=messages,
                system=system,
                response_format=response_format,
                temperature=kwargs.get("temperature"),
                max_tokens=kwargs.get("max_tokens"),
                top_p=kwargs.get("top_p"),
                stop=kwargs.get("stop"),
                tools=kwargs.get("tools"),
                tool_choice=kwargs.get("tool_choice"),
                provider_params=kwargs.get("provider_params", {}),
            )

            if effective_model:
                result = await self.text_client.execute(request, effective_model)
            else:
                result = await self.text_client.execute_with_fallback(request)

            if include_breadcrumbs:
                result.breadcrumbs = collector.get_all()

            return result

        except Exception as e:
            add_error(
                layer=SDKLayer.SDK.value,
                action="text_request_failed",
                message=f"Text/LLM request failed: {e}",
                error=str(e),
            )
            raise

    async def list_voices(
        self,
        provider: Optional[str] = None,
    ) -> Dict[str, List[VoiceInfo]]:
        """
        List available voices from all or specific provider.

        Args:
            provider: Optional provider name to filter by.
                     If None, returns voices from all registered providers.

        Returns:
            Dict mapping provider names to their available voices

        Example:
            voices = await sdk.list_voices()
            for provider, voice_list in voices.items():
                print(f"{provider}: {len(voice_list)} voices")
                for voice in voice_list[:3]:
                    print(f"  - {voice.name} ({voice.id})")
        """
        return await self.tts.get_available_voices(provider)

    def _normalize_tts_request(
        self,
        request: Union[TTSRequest, Dict[str, Any], str],
        model: Optional[str],
        kwargs: Dict[str, Any],
    ) -> TTSRequest:
        """
        Normalize various request formats to TTSRequest.

        Args:
            request: TTSRequest, dict with request fields, or plain text string
            model: Model string to use (overrides request model)
            kwargs: Additional parameters to merge

        Returns:
            Normalized TTSRequest instance
        """
        if isinstance(request, str):
            # Plain text string
            return TTSRequest(
                text=request,
                model=model,
                **kwargs,
            )
        elif isinstance(request, dict):
            # Dict with request fields
            merged = {**request, **kwargs}
            if model:
                merged["model"] = model
            return TTSRequest.from_dict(merged)
        else:
            # Already TTSRequest
            if model:
                return request.merge({"model": model, **kwargs})
            elif kwargs:
                return request.merge(kwargs)
            return request

    @classmethod
    def from_env(cls) -> "UnifiedAI":
        """
        Create SDK instance from environment variables.

        Reads API keys from standard environment variables:
        - OPENAI_API_KEY
        - ANTHROPIC_API_KEY
        - GOOGLE_API_KEY (for Gemini)
        - ELEVENLABS_API_KEY

        Returns:
            UnifiedAI instance configured from environment

        Example:
            import os
            os.environ["ELEVENLABS_API_KEY"] = "xi-..."
            os.environ["GOOGLE_API_KEY"] = "..."

            sdk = UnifiedAI.from_env()
        """
        config = Config.from_env()
        return cls(config)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UnifiedAI":
        """
        Create SDK instance from configuration dictionary.

        Args:
            data: Configuration dictionary (see Config.from_dict for schema)

        Returns:
            UnifiedAI instance

        Example:
            sdk = UnifiedAI.from_dict({
                "providers": {
                    "elevenlabs": {"api_key": "xi-..."},
                    "gemini": {"api_key": "..."},
                },
                "defaults": {"tts": "elevenlabs/eleven_multilingual_v2"},
            })
        """
        config = Config.from_dict(data)
        return cls(config)

    async def close(self) -> None:
        """
        Close SDK and release resources.

        Should be called when done using the SDK to clean up any
        open connections or resources.
        """
        self._tts_client = None

    async def __aenter__(self) -> "UnifiedAI":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()


__all__ = ["UnifiedAI"]
