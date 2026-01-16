"""
Basic tests for Unified AI SDK
Uses minimal prompts to conserve API credits
"""
import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch


class TestBreadcrumbs:
    """Test breadcrumb system without external dependencies"""

    def test_breadcrumb_level_enum(self):
        from unified_ai.breadcrumbs import BreadcrumbLevel
        assert BreadcrumbLevel.SUCCESS == "SUCCESS"
        assert BreadcrumbLevel.INFO == "INFO"
        assert BreadcrumbLevel.WARN == "WARN"
        assert BreadcrumbLevel.ERROR == "ERROR"

    def test_sdk_layer_enum(self):
        from unified_ai.breadcrumbs import SDKLayer
        assert SDKLayer.SDK == "SDK"
        assert SDKLayer.CLIENT == "Client"
        assert SDKLayer.ADAPTER == "Adapter"

    def test_breadcrumb_collector(self):
        from unified_ai.breadcrumbs import BreadcrumbCollector, BreadcrumbLevel

        collector = BreadcrumbCollector(request_id="test-123")
        collector.add("SDK", "test_action", BreadcrumbLevel.INFO, "Test message")

        breadcrumbs = collector.get_all()
        assert len(breadcrumbs) == 1
        assert breadcrumbs[0]["layer"] == "SDK"
        assert breadcrumbs[0]["action"] == "test_action"
        assert breadcrumbs[0]["level"] == "INFO"

    def test_context_var_collection(self):
        from unified_ai.breadcrumbs import (
            start_collection, get_collector, add_info, add_success
        )

        collector = start_collection("ctx-test-456")
        assert get_collector() == collector

        add_info("SDK", "start", "Starting request")
        add_success("SDK", "end", "Request completed")

        breadcrumbs = collector.get_all()
        assert len(breadcrumbs) == 2
        assert breadcrumbs[0]["level"] == "INFO"
        assert breadcrumbs[1]["level"] == "SUCCESS"


class TestConfig:
    """Test configuration system"""

    def test_provider_config(self):
        from unified_ai.config import ProviderConfig

        config = ProviderConfig(api_key="test-key")
        assert config.api_key == "test-key"
        assert config.enabled is True
        assert config.timeout_seconds == 30
        assert config.max_retries == 3

    def test_fallback_config(self):
        from unified_ai.config import FallbackConfig

        config = FallbackConfig(
            tts=["elevenlabs/eleven_multilingual_v2", "gemini/gemini-2.0-flash"]
        )
        assert len(config.tts) == 2
        assert "elevenlabs" in config.tts[0]

    def test_config_from_dict(self):
        from unified_ai.config import Config

        data = {
            "providers": {
                "elevenlabs": {"api_key": "el-key"},
                "gemini": {"api_key": "gem-key"}
            },
            "fallback": {
                "tts": ["elevenlabs/eleven_multilingual_v2"]
            }
        }
        config = Config.from_dict(data)

        assert "elevenlabs" in config.providers
        assert config.providers["elevenlabs"].api_key == "el-key"
        assert len(config.fallback.tts) == 1


class TestTypes:
    """Test type definitions"""

    def test_audio_format_enum(self):
        from unified_ai.models import AudioFormat
        assert AudioFormat.MP3.value == "mp3"
        assert AudioFormat.WAV.value == "wav"
        assert AudioFormat.OGG.value == "ogg"

    def test_capability_enum(self):
        from unified_ai.models import Capability
        assert Capability.TTS.name == "TTS"
        assert Capability.TEXT.name == "TEXT"

    def test_tts_request(self):
        from unified_ai.models import TTSRequest, AudioFormat

        request = TTSRequest(
            text="Hello",  # Minimal text
            voice="Kore"
        )
        assert request.text == "Hello"
        assert request.voice == "Kore"
        assert request.output_format == AudioFormat.MP3


class TestExceptions:
    """Test exception hierarchy"""

    def test_sdk_error(self):
        from unified_ai.exceptions import SDKError

        error = SDKError(message="Test error")
        assert str(error) == "Test error"
        assert error.recommendations == []

    def test_rate_limit_error(self):
        from unified_ai.exceptions import RateLimitError

        error = RateLimitError(
            message="Rate limited",
            provider="elevenlabs",
            model="eleven_multilingual_v2",
            retry_after_seconds=30
        )
        assert error.retry_strategy["is_retryable"] is True
        assert error.retry_after_seconds == 30

    def test_quota_exceeded_error(self):
        from unified_ai.exceptions import QuotaExceededError

        error = QuotaExceededError(
            message="Quota exceeded",
            provider="elevenlabs",
            model="eleven_multilingual_v2"
        )
        assert error.retry_strategy["is_retryable"] is False

    def test_all_providers_failed_error(self):
        from unified_ai.exceptions import AllProvidersFailedError

        error = AllProvidersFailedError(
            message="All failed",
            failed_providers=[
                {"provider": "elevenlabs", "error": "timeout"},
                {"provider": "gemini", "error": "rate_limit"}
            ]
        )
        assert len(error.failed_providers) == 2


class TestRetryStrategy:
    """Test retry logic"""

    def test_no_retry_errors(self):
        from unified_ai.utils.retry import SafeRetryStrategy

        strategy = SafeRetryStrategy()

        # 401 should NOT retry (bad API key)
        should_retry, _ = strategy.should_retry(401, 0)
        assert should_retry is False

        # 402 should NOT retry (out of credits)
        should_retry, _ = strategy.should_retry(402, 0)
        assert should_retry is False

    def test_retryable_errors(self):
        from unified_ai.utils.retry import SafeRetryStrategy

        strategy = SafeRetryStrategy()

        # 429 should retry with wait
        should_retry, wait = strategy.should_retry(429, 0)
        assert should_retry is True
        assert wait == 10

        # 503 should retry with exponential backoff
        should_retry, wait = strategy.should_retry(503, 0)
        assert should_retry is True
        assert wait > 0

    def test_max_retries_exceeded(self):
        from unified_ai.utils.retry import SafeRetryStrategy

        strategy = SafeRetryStrategy()

        # Even 503 should not retry after max attempts
        should_retry, _ = strategy.should_retry(503, 3, max_retries=3)
        assert should_retry is False


class TestAudioUtils:
    """Test audio conversion utilities"""

    def test_pcm_to_wav(self):
        from unified_ai.utils.audio import pcm_to_wav

        # Create minimal PCM data (silence)
        pcm_data = bytes(4800)  # 0.1s of 24kHz mono 16-bit silence
        wav_data = pcm_to_wav(pcm_data, sample_rate=24000)

        # WAV files start with RIFF header
        assert wav_data[:4] == b"RIFF"
        assert b"WAVE" in wav_data[:12]


class TestAdapterRegistry:
    """Test adapter registration"""

    def test_registry_operations(self):
        from unified_ai.clients.base import AdapterRegistry
        from unified_ai.adapters.base import BaseAdapter, Capability

        # Create mock adapter
        class MockAdapter(BaseAdapter):
            name = "mock"

            @property
            def capabilities(self):
                return {Capability.TTS}

            def _init_client(self):
                return None

        registry = AdapterRegistry()
        adapter = MockAdapter(api_key="test")

        registry.register(adapter)

        assert registry.get("mock") == adapter
        assert "mock" in registry.list_providers()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
