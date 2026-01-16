"""
Integration tests for Unified AI SDK
Tests the full SDK flow with mocked API responses
Uses minimal prompts ("Hi") to conserve credits if real APIs are used
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import os


class TestUnifiedAIIntegration:
    """Integration tests for the complete SDK flow"""

    @pytest.fixture
    def mock_config(self):
        """Create test configuration"""
        from unified_ai.config import Config, ProviderConfig, FallbackConfig

        return Config(
            providers={
                "elevenlabs": ProviderConfig(api_key="test-el-key"),
                "gemini": ProviderConfig(api_key="test-gem-key"),
            },
            fallback=FallbackConfig(
                tts=["elevenlabs/eleven_multilingual_v2", "gemini/gemini-2.0-flash"]
            ),
            defaults={"tts": "elevenlabs/eleven_multilingual_v2"}
        )

    @pytest.fixture
    def mock_config_no_default(self):
        """Config without defaults - forces fallback chain"""
        from unified_ai.config import Config, ProviderConfig, FallbackConfig

        return Config(
            providers={
                "elevenlabs": ProviderConfig(api_key="test-el-key"),
                "gemini": ProviderConfig(api_key="test-gem-key"),
            },
            fallback=FallbackConfig(
                tts=["elevenlabs/eleven_multilingual_v2", "gemini/gemini-2.0-flash"]
            ),
            defaults={}  # No defaults - forces execute_with_fallback
        )

    @pytest.fixture
    def sdk(self, mock_config):
        """Create SDK instance"""
        from unified_ai import UnifiedAI
        return UnifiedAI(mock_config)

    def test_sdk_initialization(self, mock_config):
        """Test SDK initializes with correct adapters"""
        from unified_ai import UnifiedAI

        sdk = UnifiedAI(mock_config)

        assert sdk.config == mock_config
        assert sdk._registry is not None
        assert sdk._tts_client is not None

    def test_adapter_registration(self, sdk):
        """Test adapters are registered correctly"""
        providers = sdk._registry.list_providers()

        # Both providers should be registered
        assert "elevenlabs" in providers
        assert "gemini" in providers

    def test_tts_client_fallback_chain(self, sdk):
        """Test TTS client has correct fallback chain"""
        tts_client = sdk.tts

        assert len(tts_client.fallback_chain) == 2
        assert "elevenlabs" in tts_client.fallback_chain[0]
        assert "gemini" in tts_client.fallback_chain[1]

    @pytest.mark.asyncio
    async def test_generate_speech_with_mock(self, sdk):
        """Test generate_speech flow with mocked API"""
        from unified_ai.models import AudioFormat, RawAudioResponse

        # Mock the adapter's tts method
        mock_audio = b"fake_audio_data_mp3"
        mock_response = RawAudioResponse(
            data=mock_audio,
            format=AudioFormat.MP3,
            sample_rate=44100,
            channels=1
        )

        with patch.object(
            sdk._registry.get("elevenlabs"),
            'tts',
            new_callable=AsyncMock,
            return_value=mock_response
        ):
            # Use minimal text to conserve credits
            response = await sdk.generate_speech(
                text="Hi",  # Minimal prompt!
                voice="test-voice",
                model="elevenlabs/eleven_multilingual_v2"
            )

            assert response.success
            assert response.audio.data == mock_audio
            assert response.breadcrumbs is not None
            assert len(response.breadcrumbs) > 0

    @pytest.mark.asyncio
    async def test_fallback_chain_execution(self, mock_config_no_default):
        """Test fallback chain triggers on primary failure"""
        from unified_ai import UnifiedAI
        from unified_ai.models import AudioFormat, RawAudioResponse
        from unified_ai.exceptions import ProviderError

        # SDK with no defaults to force fallback chain
        sdk = UnifiedAI(mock_config_no_default)

        mock_audio = b"gemini_audio_data"
        mock_response = RawAudioResponse(
            data=mock_audio,
            format=AudioFormat.MP3,
            sample_rate=24000,
            channels=1
        )

        # ElevenLabs fails, Gemini succeeds
        elevenlabs_adapter = sdk._registry.get("elevenlabs")
        gemini_adapter = sdk._registry.get("gemini")

        with patch.object(
            elevenlabs_adapter,
            'tts',
            new_callable=AsyncMock,
            side_effect=ProviderError(
                message="Rate limit",
                provider="elevenlabs",
                model="eleven_multilingual_v2",
                http_status=429
            )
        ), patch.object(
            gemini_adapter,
            'tts',
            new_callable=AsyncMock,
            return_value=mock_response
        ):
            # No model + no defaults = execute_with_fallback()
            response = await sdk.generate_speech(
                text="Hi",  # Minimal prompt!
                voice="Kore"
            )

            assert response.success
            assert response.provider == "gemini"

            # Check breadcrumbs show fallback
            breadcrumb_actions = [bc.get("action") for bc in response.breadcrumbs]
            assert "fallback_triggered" in breadcrumb_actions or any(
                "fallback" in str(bc) for bc in response.breadcrumbs
            )

    @pytest.mark.asyncio
    async def test_all_providers_failed_error(self, mock_config_no_default):
        """Test AllProvidersFailedError when all providers fail"""
        from unified_ai import UnifiedAI
        from unified_ai.exceptions import ProviderError, AllProvidersFailedError

        # SDK with no defaults to force fallback chain
        sdk = UnifiedAI(mock_config_no_default)

        # Both providers fail
        with patch.object(
            sdk._registry.get("elevenlabs"),
            'tts',
            new_callable=AsyncMock,
            side_effect=ProviderError(
                message="Error 1",
                provider="elevenlabs",
                model="test"
            )
        ), patch.object(
            sdk._registry.get("gemini"),
            'tts',
            new_callable=AsyncMock,
            side_effect=ProviderError(
                message="Error 2",
                provider="gemini",
                model="test"
            )
        ):
            with pytest.raises(AllProvidersFailedError) as exc_info:
                await sdk.generate_speech(
                    text="Hi",  # Minimal prompt!
                    voice="test"
                )

            error = exc_info.value
            assert len(error.failed_providers) == 2
            assert error.breadcrumbs is not None

    @pytest.mark.asyncio
    async def test_breadcrumb_collection(self, sdk):
        """Test breadcrumbs are collected throughout execution"""
        from unified_ai.models import AudioFormat, RawAudioResponse
        from unified_ai.breadcrumbs import BreadcrumbLevel

        mock_response = RawAudioResponse(
            data=b"audio",
            format=AudioFormat.MP3,
            sample_rate=44100,
            channels=1
        )

        with patch.object(
            sdk._registry.get("elevenlabs"),
            'tts',
            new_callable=AsyncMock,
            return_value=mock_response
        ):
            response = await sdk.generate_speech(
                text="Hi",  # Minimal prompt!
                voice="test",
                model="elevenlabs/eleven_multilingual_v2"
            )

            # Check breadcrumbs structure
            assert response.breadcrumbs is not None

            for bc in response.breadcrumbs:
                assert "timestamp" in bc
                assert "layer" in bc
                assert "action" in bc
                assert "level" in bc

    def test_config_from_env(self):
        """Test Config.from_env() loads environment variables"""
        from unified_ai.config import Config

        # Set test env vars
        with patch.dict(os.environ, {
            "ELEVENLABS_API_KEY": "test-el-key",
            "GOOGLE_API_KEY": "test-gem-key",
        }):
            config = Config.from_env()

            assert "elevenlabs" in config.providers
            assert config.providers["elevenlabs"].api_key == "test-el-key"


class TestRealAPIIntegration:
    """
    Tests with real API calls - ONLY RUN WITH VALID API KEYS
    Uses minimal prompts ("Hi") to conserve credits
    """

    @pytest.fixture
    def real_sdk(self):
        """Create SDK with real API keys from environment"""
        from unified_ai import UnifiedAI, Config

        el_key = os.environ.get("ELEVENLABS_API_KEY")
        gem_key = os.environ.get("GOOGLE_API_KEY")

        if not el_key and not gem_key:
            pytest.skip("No API keys set - skipping real API tests")

        return UnifiedAI.from_env()

    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not os.environ.get("ELEVENLABS_API_KEY"),
        reason="ELEVENLABS_API_KEY not set"
    )
    async def test_real_elevenlabs_tts(self, real_sdk):
        """Test real ElevenLabs TTS - MINIMAL PROMPT"""
        response = await real_sdk.generate_speech(
            text="Hi",  # Minimal to save credits!
            voice="Rachel",
            model="elevenlabs/eleven_multilingual_v2"
        )

        assert response.success
        assert response.audio.data is not None
        assert len(response.audio.data) > 0
        assert response.provider == "elevenlabs"

    @pytest.mark.asyncio
    @pytest.mark.skipif(
        not os.environ.get("GOOGLE_API_KEY"),
        reason="GOOGLE_API_KEY not set"
    )
    async def test_real_gemini_tts(self, real_sdk):
        """Test real Gemini TTS - MINIMAL PROMPT"""
        response = await real_sdk.generate_speech(
            text="Hi",  # Minimal to save credits!
            voice="Kore",
            model="gemini/gemini-2.0-flash"
        )

        assert response.success
        assert response.audio.data is not None
        assert len(response.audio.data) > 0
        assert response.provider == "gemini"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-k", "not real"])
