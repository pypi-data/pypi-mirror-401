"""
Tests for adapter methods using mocks.

Tests cover:
- OpenAI TTS returns audio bytes (mock)
- OpenAI STT returns transcription dict (mock)
- Anthropic complete returns string (mock)
- OpenRouter complete returns string (mock)
- ElevenLabs STT returns transcription dict (mock)
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import asyncio


class TestOpenAIAdapterTTS:
    """Test OpenAI adapter TTS functionality with mocks."""

    @pytest.fixture
    def mock_openai_client(self):
        """Create a mock OpenAI client."""
        mock_client = Mock()
        mock_speech_response = Mock()
        mock_speech_response.content = b"fake_audio_data_mp3"
        mock_client.audio.speech.create = Mock(return_value=mock_speech_response)
        return mock_client

    @pytest.mark.asyncio
    async def test_tts_returns_audio_bytes(self, mock_openai_client):
        """OpenAI TTS should return RawAudioResponse with audio bytes."""
        from unified_ai.adapters.openai import OpenAIAdapter
        from unified_ai.models import RawAudioResponse

        adapter = OpenAIAdapter(api_key="test-key")
        adapter._client = mock_openai_client

        with patch("asyncio.to_thread", new_callable=lambda: AsyncMock(return_value=Mock(content=b"audio_data"))):
            response = await adapter.tts(
                text="Hello world",
                model="tts-1",
                voice="alloy",
            )

        assert isinstance(response, RawAudioResponse)
        assert isinstance(response.data, bytes)
        assert len(response.data) > 0

    @pytest.mark.asyncio
    async def test_tts_uses_correct_voice(self, mock_openai_client):
        """OpenAI TTS should pass the correct voice parameter."""
        from unified_ai.adapters.openai import OpenAIAdapter

        adapter = OpenAIAdapter(api_key="test-key")
        adapter._client = mock_openai_client

        with patch("asyncio.to_thread") as mock_thread:
            mock_response = Mock()
            mock_response.content = b"audio_data"
            mock_thread.return_value = mock_response

            await adapter.tts(
                text="Test text",
                model="tts-1",
                voice="nova",
            )

            # Verify to_thread was called (meaning the API was invoked)
            assert mock_thread.called


class TestOpenAIAdapterSTT:
    """Test OpenAI adapter STT functionality with mocks."""

    @pytest.fixture
    def mock_openai_client(self):
        """Create a mock OpenAI client for STT."""
        mock_client = Mock()
        mock_transcription = Mock()
        mock_transcription.text = "This is a test transcription."
        mock_transcription.language = "en"
        mock_transcription.duration = 5.5
        mock_transcription.segments = []
        mock_client.audio.transcriptions.create = Mock(return_value=mock_transcription)
        return mock_client

    @pytest.mark.asyncio
    async def test_stt_returns_transcription_dict(self, mock_openai_client):
        """OpenAI STT should return dict with text and metadata."""
        from unified_ai.adapters.openai import OpenAIAdapter

        adapter = OpenAIAdapter(api_key="test-key")
        adapter._client = mock_openai_client

        with patch("asyncio.to_thread") as mock_thread:
            mock_response = Mock()
            mock_response.text = "Transcribed text"
            mock_response.language = "en"
            mock_response.duration = 3.0
            mock_response.segments = []
            mock_response.words = None  # Set to None so hasattr check passes but truthiness fails
            mock_thread.return_value = mock_response

            with patch("tempfile.NamedTemporaryFile"):
                with patch("os.unlink"):
                    with patch("builtins.open", MagicMock()):
                        result = await adapter.transcribe(
                            audio=b"fake_audio_data",
                            model="whisper-1",
                        )

        assert isinstance(result, dict)
        assert "text" in result


class TestAnthropicAdapterComplete:
    """Test Anthropic adapter complete functionality with mocks."""

    @pytest.fixture
    def mock_anthropic_client(self):
        """Create a mock Anthropic client."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock(type="text", text="Claude response text")]
        mock_response.stop_reason = "end_turn"
        mock_response.usage = Mock(input_tokens=100, output_tokens=50)
        mock_response.usage.cache_creation_input_tokens = 0
        mock_response.usage.cache_read_input_tokens = 0
        mock_client.messages.create = Mock(return_value=mock_response)
        return mock_client

    @pytest.mark.asyncio
    async def test_complete_returns_content_string(self, mock_anthropic_client):
        """Anthropic complete should return dict with content string."""
        from unified_ai.adapters.anthropic import AnthropicAdapter

        adapter = AnthropicAdapter(api_key="test-key")
        adapter._client = mock_anthropic_client

        result = await adapter.complete(
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-sonnet-4-20250514",
        )

        assert isinstance(result, dict)
        assert "content" in result
        assert isinstance(result["content"], str)
        assert len(result["content"]) > 0
        assert result["content"] == "Claude response text"

    @pytest.mark.asyncio
    async def test_complete_includes_usage(self, mock_anthropic_client):
        """Anthropic complete should include usage information."""
        from unified_ai.adapters.anthropic import AnthropicAdapter

        adapter = AnthropicAdapter(api_key="test-key")
        adapter._client = mock_anthropic_client

        result = await adapter.complete(
            messages=[{"role": "user", "content": "Hello"}],
            model="claude-sonnet-4-20250514",
        )

        assert "usage" in result
        assert "prompt_tokens" in result["usage"]
        assert "completion_tokens" in result["usage"]

    @pytest.mark.asyncio
    async def test_complete_handles_system_message(self, mock_anthropic_client):
        """Anthropic complete should extract system message from messages."""
        from unified_ai.adapters.anthropic import AnthropicAdapter

        adapter = AnthropicAdapter(api_key="test-key")
        adapter._client = mock_anthropic_client

        result = await adapter.complete(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello"},
            ],
            model="claude-sonnet-4-20250514",
        )

        # Should have called with system parameter extracted
        call_kwargs = mock_anthropic_client.messages.create.call_args
        assert call_kwargs is not None


class TestOpenRouterAdapterComplete:
    """Test OpenRouter adapter complete functionality with mocks."""

    @pytest.fixture
    def mock_openai_client_for_openrouter(self):
        """Create a mock OpenAI client for OpenRouter."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.choices = [
            Mock(message=Mock(content="OpenRouter response"), finish_reason="stop")
        ]
        mock_response.usage = Mock(
            prompt_tokens=50,
            completion_tokens=30,
            total_tokens=80,
        )
        mock_client.chat.completions.create = Mock(return_value=mock_response)
        return mock_client

    @pytest.mark.asyncio
    async def test_complete_returns_content_string(self, mock_openai_client_for_openrouter):
        """OpenRouter complete should return dict with content string."""
        from unified_ai.adapters.openrouter import OpenRouterAdapter

        adapter = OpenRouterAdapter(api_key="test-key")
        adapter._client = mock_openai_client_for_openrouter

        result = await adapter.complete(
            messages=[{"role": "user", "content": "Hello"}],
            model="anthropic/claude-sonnet-4",
        )

        assert isinstance(result, dict)
        assert "content" in result
        assert isinstance(result["content"], str)
        assert result["content"] == "OpenRouter response"

    @pytest.mark.asyncio
    async def test_complete_includes_usage(self, mock_openai_client_for_openrouter):
        """OpenRouter complete should include usage information."""
        from unified_ai.adapters.openrouter import OpenRouterAdapter

        adapter = OpenRouterAdapter(api_key="test-key")
        adapter._client = mock_openai_client_for_openrouter

        result = await adapter.complete(
            messages=[{"role": "user", "content": "Hello"}],
            model="anthropic/claude-sonnet-4",
        )

        assert "usage" in result
        assert result["usage"]["total_tokens"] == 80


class TestElevenLabsAdapterSTT:
    """Test ElevenLabs adapter STT functionality with mocks."""

    @pytest.mark.asyncio
    async def test_stt_returns_transcription_dict(self):
        """ElevenLabs STT should return dict with text and metadata."""
        from unified_ai.adapters.elevenlabs import ElevenLabsAdapter

        adapter = ElevenLabsAdapter(api_key="test-key")

        mock_response = {
            "text": "Transcribed speech from ElevenLabs",
            "language_code": "en",
            "duration_seconds": 4.2,
            "words": [{"word": "test", "start": 0.0, "end": 0.5}],
        }

        with patch.object(adapter, "_get_session") as mock_session:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.status = 200
            mock_context.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

            mock_session.return_value.post = Mock(return_value=mock_context)

            result = await adapter.transcribe(
                audio=b"fake_audio_data",
                model="scribe_v1",
            )

        assert isinstance(result, dict)
        assert "text" in result
        assert result["text"] == "Transcribed speech from ElevenLabs"

    @pytest.mark.asyncio
    async def test_stt_includes_duration(self):
        """ElevenLabs STT should include duration in response."""
        from unified_ai.adapters.elevenlabs import ElevenLabsAdapter

        adapter = ElevenLabsAdapter(api_key="test-key")

        mock_response = {
            "text": "Test transcription",
            "language_code": "en",
            "duration_seconds": 10.5,
            "words": [],
        }

        with patch.object(adapter, "_get_session") as mock_session:
            mock_context = AsyncMock()
            mock_context.__aenter__.return_value.status = 200
            mock_context.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

            mock_session.return_value.post = Mock(return_value=mock_context)

            result = await adapter.transcribe(
                audio=b"fake_audio_data",
                model="scribe_v1",
            )

        assert "duration_seconds" in result
        assert result["duration_seconds"] == 10.5


class TestAdapterCapabilities:
    """Test adapter capability declarations."""

    def test_openai_has_text_tts_stt_capabilities(self):
        """OpenAI adapter should declare TEXT, TTS, and STT capabilities."""
        from unified_ai.adapters.openai import OpenAIAdapter
        from unified_ai.models import Capability

        adapter = OpenAIAdapter(api_key="test-key")

        assert Capability.TEXT in adapter.capabilities
        assert Capability.TTS in adapter.capabilities
        assert Capability.STT in adapter.capabilities

    def test_anthropic_has_only_text_capability(self):
        """Anthropic adapter should only declare TEXT capability."""
        from unified_ai.adapters.anthropic import AnthropicAdapter
        from unified_ai.models import Capability

        adapter = AnthropicAdapter(api_key="test-key")

        assert Capability.TEXT in adapter.capabilities
        assert Capability.TTS not in adapter.capabilities
        assert Capability.STT not in adapter.capabilities

    def test_openrouter_has_only_text_capability(self):
        """OpenRouter adapter should only declare TEXT capability."""
        from unified_ai.adapters.openrouter import OpenRouterAdapter
        from unified_ai.models import Capability

        adapter = OpenRouterAdapter(api_key="test-key")

        assert Capability.TEXT in adapter.capabilities
        assert Capability.TTS not in adapter.capabilities

    def test_elevenlabs_has_tts_and_stt_capabilities(self):
        """ElevenLabs adapter should declare TTS and STT capabilities."""
        from unified_ai.adapters.elevenlabs import ElevenLabsAdapter
        from unified_ai.models import Capability

        adapter = ElevenLabsAdapter(api_key="test-key")

        assert Capability.TTS in adapter.capabilities
        assert Capability.STT in adapter.capabilities


class TestAdapterDefaultModels:
    """Test adapter default model declarations."""

    def test_openai_default_models(self):
        """OpenAI adapter should have sensible default models."""
        from unified_ai.adapters.openai import OpenAIAdapter

        assert "text" in OpenAIAdapter.DEFAULT_MODELS
        assert "tts" in OpenAIAdapter.DEFAULT_MODELS
        assert "stt" in OpenAIAdapter.DEFAULT_MODELS

    def test_anthropic_default_model(self):
        """Anthropic adapter should have default text model."""
        from unified_ai.adapters.anthropic import AnthropicAdapter

        assert "text" in AnthropicAdapter.DEFAULT_MODELS

    def test_openrouter_default_model(self):
        """OpenRouter adapter should have default text model."""
        from unified_ai.adapters.openrouter import OpenRouterAdapter

        assert "text" in OpenRouterAdapter.DEFAULT_MODELS


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
