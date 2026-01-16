"""
Unified AI SDK - Multi-provider AI abstraction layer

Usage:
    from unified_ai import UnifiedAI, Config

    # From environment variables
    sdk = UnifiedAI.from_env()

    # Or with explicit config
    config = Config(
        providers={
            "elevenlabs": ProviderConfig(api_key="sk-..."),
            "gemini": ProviderConfig(api_key="AIza..."),
        },
        fallback=FallbackConfig(
            tts=["elevenlabs/eleven_multilingual_v2", "gemini/gemini-2.0-flash"]
        )
    )
    sdk = UnifiedAI(config)

    # Generate speech
    response = await sdk.generate_speech("Hello world", voice="Kore")
    response.audio.save("output.mp3")
"""

# Version
__version__ = "0.1.0"

# Main SDK class
from .sdk import UnifiedAI

# Configuration
from .config import Config, ProviderConfig, FallbackConfig, RetryConfig

# Types
from .models import (
    AudioFormat,
    Capability,
    TTSRequest,
    TTSResponse,
    TextRequest,
    TextResponse,
    RawAudioResponse,
    VoiceInfo,
)

# Exceptions
from .exceptions import (
    SDKError,
    ProviderError,
    RateLimitError,
    QuotaExceededError,
    AllProvidersFailedError,
    ValidationError,
    ConfigurationError,
)

# Breadcrumbs (for advanced usage)
from .breadcrumbs import (
    BreadcrumbLevel,
    BreadcrumbCollector,
    start_collection,
    get_collector,
)

# Clients (for advanced usage)
from .clients import AdapterRegistry, UnifiedTTSClient, UnifiedTextClient

# Adapters (for advanced usage / custom registration)
from .adapters import BaseAdapter, ElevenLabsAdapter, GeminiAdapter

# Presets
from .presets import TTSPreset, load_preset, list_presets


def help() -> str:
    """Print SDK help and quick start guide."""
    help_text = """
Unified AI SDK - Multi-provider TTS abstraction layer
======================================================

QUICK START:
    from unified_ai import UnifiedAI, Config, ProviderConfig

    config = Config(providers={
        "gemini": ProviderConfig(api_key="AIza..."),
        "elevenlabs": ProviderConfig(api_key="sk_..."),
    })
    sdk = UnifiedAI(config)

    # With preset (recommended)
    response = await sdk.generate_speech(text, preset="gemini/turov_channel")
    response.audio.save("output.mp3")

PRESETS:
    from unified_ai import list_presets
    print(list_presets())  # Show all available presets

    Gemini:     gemini/turov_channel, gemini/warm_trainer, gemini/narrator_fast
    ElevenLabs: elevenlabs/turov, elevenlabs/george

VOICES:
    voices = await sdk.list_voices()  # Get available voices per provider

PARAMETERS:
    await sdk.generate_speech(
        text,
        preset="gemini/turov_channel",  # OR explicit voice/model
        voice="Enceladus",
        model="gemini/gemini-2.5-pro-preview-tts",
        output_format="mp3",            # mp3, wav, ogg
        provider_params={"temperature": 1.35, "streaming": True}
    )

DOCS: See README.md in unified_ai/ folder
"""
    print(help_text)
    return help_text


__all__ = [
    # Version
    "__version__",
    # Main
    "UnifiedAI",
    # Config
    "Config",
    "ProviderConfig",
    "FallbackConfig",
    "RetryConfig",
    # Types
    "AudioFormat",
    "Capability",
    "TTSRequest",
    "TTSResponse",
    "TextRequest",
    "TextResponse",
    "RawAudioResponse",
    "VoiceInfo",
    # Exceptions
    "SDKError",
    "ProviderError",
    "RateLimitError",
    "QuotaExceededError",
    "AllProvidersFailedError",
    "ValidationError",
    "ConfigurationError",
    # Breadcrumbs
    "BreadcrumbLevel",
    "BreadcrumbCollector",
    "start_collection",
    "get_collector",
    # Clients
    "AdapterRegistry",
    "UnifiedTTSClient",
    "UnifiedTextClient",
    # Adapters
    "BaseAdapter",
    "ElevenLabsAdapter",
    "GeminiAdapter",
    # Presets
    "TTSPreset",
    "load_preset",
    "list_presets",
    # Help
    "help",
]
