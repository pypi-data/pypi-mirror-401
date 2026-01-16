"""
Configuration module for Unified AI SDK.

Provides dataclasses for configuring providers, retry behavior,
fallback chains, and global SDK settings.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import os


@dataclass
class ProviderConfig:
    """Configuration for a single provider."""

    api_key: str
    enabled: bool = True
    timeout_seconds: int = 30
    max_retries: int = 3
    endpoint: Optional[str] = None  # For custom endpoints


@dataclass
class RetryConfig:
    """Configuration for retry behavior with exponential backoff."""

    max_retries: int = 3
    initial_delay_seconds: float = 1.0
    max_delay_seconds: float = 30.0
    exponential_base: float = 2.0
    retryable_status_codes: List[int] = field(
        default_factory=lambda: [429, 500, 502, 503, 504]
    )


@dataclass
class FallbackConfig:
    """Configuration for fallback chains per capability."""

    tts: List[str] = field(default_factory=list)
    text: List[str] = field(default_factory=list)
    embed: List[str] = field(default_factory=list)
    stt: List[str] = field(default_factory=list)
    image: List[str] = field(default_factory=list)
    vision: List[str] = field(default_factory=list)


@dataclass
class Config:
    """
    Main configuration for Unified AI SDK.

    Example usage:
        config = Config(
            providers={
                "openai": ProviderConfig(api_key="sk-..."),
                "elevenlabs": ProviderConfig(api_key="xi-..."),
            },
            defaults={"tts": "elevenlabs/eleven_multilingual_v2"},
            fallback=FallbackConfig(
                tts=["elevenlabs/eleven_multilingual_v2", "openai/tts-1"]
            ),
        )
    """

    providers: Dict[str, ProviderConfig] = field(default_factory=dict)
    fallback: FallbackConfig = field(default_factory=FallbackConfig)
    retry: RetryConfig = field(default_factory=RetryConfig)
    defaults: Dict[str, str] = field(default_factory=dict)
    include_breadcrumbs: bool = True

    def get_provider_config(self, name: str) -> Optional[ProviderConfig]:
        """
        Get configuration for a specific provider.

        Args:
            name: Provider name (e.g., "openai", "elevenlabs")

        Returns:
            ProviderConfig if found and enabled, None otherwise
        """
        config = self.providers.get(name)
        if config is not None and config.enabled:
            return config
        return None

    def get_fallback_chain(self, capability: str) -> List[str]:
        """
        Get fallback chain for a capability.

        Args:
            capability: Capability name (e.g., "tts", "text", "embed")

        Returns:
            List of model strings in fallback order
        """
        return getattr(self.fallback, capability, [])

    @classmethod
    def from_env(cls) -> "Config":
        """
        Create Config from environment variables.

        Reads the following environment variables:
        - OPENAI_API_KEY
        - ANTHROPIC_API_KEY
        - GOOGLE_API_KEY (for Gemini)
        - ELEVENLABS_API_KEY
        - PLAYHT_API_KEY
        - UNIFIED_AI_TIMEOUT (default: 30)
        - UNIFIED_AI_MAX_RETRIES (default: 3)

        Returns:
            Config instance with providers configured from env vars
        """
        providers: Dict[str, ProviderConfig] = {}

        # Map of provider names to their environment variable names
        env_mapping = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "gemini": "GOOGLE_API_KEY",
            "elevenlabs": "ELEVENLABS_API_KEY",
            "playht": "PLAYHT_API_KEY",
        }

        # Global settings from env
        timeout = int(os.environ.get("UNIFIED_AI_TIMEOUT", "30"))
        max_retries = int(os.environ.get("UNIFIED_AI_MAX_RETRIES", "3"))

        for provider_name, env_var in env_mapping.items():
            api_key = os.environ.get(env_var)
            if api_key:
                providers[provider_name] = ProviderConfig(
                    api_key=api_key,
                    enabled=True,
                    timeout_seconds=timeout,
                    max_retries=max_retries,
                )

        # Default fallback chains
        fallback = FallbackConfig(
            tts=["elevenlabs/eleven_multilingual_v2", "gemini/gemini-2.0-flash", "openai/tts-1"],
            text=["anthropic/claude-sonnet-4", "openai/gpt-4o", "gemini/gemini-2.5-pro"],
            embed=["openai/text-embedding-3-small", "gemini/text-embedding-004"],
            stt=["openai/whisper-1", "gemini/gemini-2.0-flash"],
        )

        # Default models per capability
        defaults = {
            "tts": "elevenlabs/eleven_multilingual_v2",
            "text": "anthropic/claude-sonnet-4",
            "embed": "openai/text-embedding-3-small",
            "stt": "openai/whisper-1",
        }

        return cls(
            providers=providers,
            fallback=fallback,
            retry=RetryConfig(max_retries=max_retries),
            defaults=defaults,
        )

    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """
        Create Config from a dictionary.

        Expected structure:
            {
                "providers": {
                    "openai": {"api_key": "sk-...", "enabled": True, ...},
                    ...
                },
                "fallback": {
                    "tts": ["provider/model", ...],
                    ...
                },
                "retry": {
                    "max_retries": 3,
                    ...
                },
                "defaults": {
                    "tts": "provider/model",
                    ...
                },
                "include_breadcrumbs": True
            }

        Args:
            data: Dictionary with configuration data

        Returns:
            Config instance
        """
        providers: Dict[str, ProviderConfig] = {}
        providers_data = data.get("providers", {})
        for name, provider_data in providers_data.items():
            if isinstance(provider_data, dict):
                providers[name] = ProviderConfig(
                    api_key=provider_data.get("api_key", ""),
                    enabled=provider_data.get("enabled", True),
                    timeout_seconds=provider_data.get("timeout_seconds", 30),
                    max_retries=provider_data.get("max_retries", 3),
                    endpoint=provider_data.get("endpoint"),
                )

        fallback_data = data.get("fallback", {})
        fallback = FallbackConfig(
            tts=fallback_data.get("tts", []),
            text=fallback_data.get("text", []),
            embed=fallback_data.get("embed", []),
            stt=fallback_data.get("stt", []),
            image=fallback_data.get("image", []),
            vision=fallback_data.get("vision", []),
        )

        retry_data = data.get("retry", {})
        retry = RetryConfig(
            max_retries=retry_data.get("max_retries", 3),
            initial_delay_seconds=retry_data.get("initial_delay_seconds", 1.0),
            max_delay_seconds=retry_data.get("max_delay_seconds", 30.0),
            exponential_base=retry_data.get("exponential_base", 2.0),
            retryable_status_codes=retry_data.get(
                "retryable_status_codes", [429, 500, 502, 503, 504]
            ),
        )

        return cls(
            providers=providers,
            fallback=fallback,
            retry=retry,
            defaults=data.get("defaults", {}),
            include_breadcrumbs=data.get("include_breadcrumbs", True),
        )
