"""
Tests for provider configuration loading and validation.

Tests cover:
- All 5 provider configs load successfully
- Config version is "1.0"
- Required fields present (provider, services)
- Pricing fields have currency and effective_date
"""
import pytest
from unified_ai.configs import get_provider_config


class TestProviderConfigLoader:
    """Test provider configuration loading."""

    PROVIDERS = ["openai", "anthropic", "elevenlabs", "gemini", "openrouter"]

    def test_all_configs_load_successfully(self):
        """All 5 provider configs should load without errors."""
        loader = get_provider_config()
        for provider in self.PROVIDERS:
            config = loader.load(provider)
            assert config is not None, f"Config for {provider} should not be None"
            assert isinstance(config, dict), f"Config for {provider} should be a dict"

    def test_config_version_is_1_0(self):
        """All configs should have config_version '1.0'."""
        loader = get_provider_config()
        for provider in self.PROVIDERS:
            config = loader.load(provider)
            assert "config_version" in config, f"{provider} missing config_version"
            assert config["config_version"] == "1.0", (
                f"{provider} config_version should be '1.0', got '{config['config_version']}'"
            )

    def test_required_fields_present(self):
        """All configs should have required fields: provider, services."""
        loader = get_provider_config()
        required_fields = ["provider", "services"]
        for provider in self.PROVIDERS:
            config = loader.load(provider)
            for field in required_fields:
                assert field in config, f"{provider} missing required field '{field}'"

    def test_provider_field_matches_filename(self):
        """The 'provider' field should match the config filename."""
        loader = get_provider_config()
        for provider in self.PROVIDERS:
            config = loader.load(provider)
            assert config["provider"] == provider, (
                f"Provider field '{config['provider']}' should match '{provider}'"
            )

    def test_services_is_dict(self):
        """The 'services' field should be a dictionary."""
        loader = get_provider_config()
        for provider in self.PROVIDERS:
            config = loader.load(provider)
            assert isinstance(config["services"], dict), (
                f"{provider} services should be a dict"
            )

    def test_nonexistent_provider_raises_error(self):
        """Loading a nonexistent provider should raise FileNotFoundError."""
        loader = get_provider_config()
        with pytest.raises(FileNotFoundError):
            loader.load("nonexistent_provider")


class TestPricingFields:
    """Test pricing field validation."""

    def test_openai_text_pricing_has_currency_and_effective_date(self):
        """OpenAI text models should have currency and effective_date in pricing."""
        loader = get_provider_config()
        config = loader.load("openai")
        text_models = config["services"]["text"]["models"]
        for model_name, model_config in text_models.items():
            pricing = model_config.get("pricing", {})
            assert "currency" in pricing, f"OpenAI {model_name} pricing missing 'currency'"
            assert "effective_date" in pricing, f"OpenAI {model_name} pricing missing 'effective_date'"
            assert pricing["currency"] == "USD", f"OpenAI {model_name} currency should be USD"

    def test_anthropic_pricing_has_currency_and_effective_date(self):
        """Anthropic models should have currency and effective_date in pricing."""
        loader = get_provider_config()
        config = loader.load("anthropic")
        text_models = config["services"]["text"]["models"]
        for model_name, model_config in text_models.items():
            pricing = model_config.get("pricing", {})
            assert "currency" in pricing, f"Anthropic {model_name} pricing missing 'currency'"
            assert "effective_date" in pricing, f"Anthropic {model_name} pricing missing 'effective_date'"

    def test_tts_pricing_has_per_1k_chars(self):
        """TTS pricing should have per_1k_chars field."""
        loader = get_provider_config()
        # Test OpenAI TTS
        openai_config = loader.load("openai")
        tts_models = openai_config["services"]["tts"]["models"]
        for model_name, model_config in tts_models.items():
            pricing = model_config.get("pricing", {})
            assert "per_1k_chars" in pricing, f"OpenAI TTS {model_name} missing 'per_1k_chars'"
            assert pricing["per_1k_chars"] > 0, f"OpenAI TTS {model_name} per_1k_chars should be > 0"

    def test_stt_pricing_has_per_minute_or_per_hour(self):
        """STT pricing should have per_minute or per_hour field."""
        loader = get_provider_config()
        # Test OpenAI STT
        openai_config = loader.load("openai")
        stt_models = openai_config["services"]["stt"]["models"]
        for model_name, model_config in stt_models.items():
            pricing = model_config.get("pricing", {})
            has_per_minute = "per_minute" in pricing
            has_per_hour = "per_hour" in pricing
            assert has_per_minute or has_per_hour, (
                f"OpenAI STT {model_name} missing 'per_minute' or 'per_hour'"
            )


class TestModelConfigAccess:
    """Test model configuration access methods."""

    def test_get_model_config_returns_dict(self):
        """get_model_config should return a dict for valid models."""
        loader = get_provider_config()
        config = loader.get_model_config("openai", "text", "gpt-4o")
        assert isinstance(config, dict)
        assert "model_id" in config

    def test_get_model_config_returns_empty_for_invalid(self):
        """get_model_config should return empty dict for invalid models."""
        loader = get_provider_config()
        config = loader.get_model_config("openai", "text", "nonexistent-model")
        assert config == {}

    def test_get_pricing_returns_dict(self):
        """get_pricing should return pricing dict for valid models."""
        loader = get_provider_config()
        pricing = loader.get_pricing("openai", "text", "gpt-4o")
        assert isinstance(pricing, dict)
        assert "input_per_1m" in pricing
        assert "output_per_1m" in pricing

    def test_get_pricing_returns_empty_for_invalid(self):
        """get_pricing should return empty dict for invalid models."""
        loader = get_provider_config()
        pricing = loader.get_pricing("openai", "text", "nonexistent-model")
        assert pricing == {}


class TestCachingBehavior:
    """Test that config loader caching works correctly."""

    def test_singleton_returns_same_instance(self):
        """get_provider_config should return the same instance."""
        loader1 = get_provider_config()
        loader2 = get_provider_config()
        assert loader1 is loader2

    def test_load_caches_results(self):
        """Loading the same provider twice should return cached result."""
        loader = get_provider_config()
        config1 = loader.load("openai")
        config2 = loader.load("openai")
        assert config1 is config2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
