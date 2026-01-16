"""
Provider configuration loader for Unified AI SDK.

Loads and caches YAML configuration files for each provider.
Provides methods to access model configs and pricing information.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from functools import lru_cache


class ProviderConfigLoader:
    """Load and cache provider YAML configs."""

    @lru_cache(maxsize=10)
    def load(self, provider: str) -> Dict[str, Any]:
        """Load provider configuration from YAML file.

        Args:
            provider: Provider name (openai, anthropic, elevenlabs, gemini, openrouter)

        Returns:
            Dictionary with provider configuration

        Raises:
            FileNotFoundError: If provider config file does not exist
        """
        config_path = Path(__file__).parent / "providers" / f"{provider}.yaml"
        with open(config_path) as f:
            return yaml.safe_load(f)

    def get_model_config(self, provider: str, service: str, model: str) -> Dict[str, Any]:
        """Get configuration for a specific model.

        Args:
            provider: Provider name
            service: Service type (text, tts, stt, diarization)
            model: Model identifier

        Returns:
            Model configuration dictionary, empty dict if not found
        """
        config = self.load(provider)
        return config["services"][service]["models"].get(model, {})

    def get_pricing(self, provider: str, service: str, model: str) -> Dict[str, float]:
        """Get pricing information for a model.

        Args:
            provider: Provider name
            service: Service type
            model: Model identifier

        Returns:
            Pricing dictionary with rates, empty dict if not found
        """
        model_config = self.get_model_config(provider, service, model)
        return model_config.get("pricing", {})


@lru_cache(maxsize=1)
def get_provider_config() -> ProviderConfigLoader:
    """Get singleton ProviderConfigLoader instance.

    Returns:
        Cached ProviderConfigLoader instance
    """
    return ProviderConfigLoader()
