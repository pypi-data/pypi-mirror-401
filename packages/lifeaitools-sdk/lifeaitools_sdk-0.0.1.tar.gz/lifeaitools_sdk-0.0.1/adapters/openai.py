"""OpenAI adapter for Unified AI SDK - Text/LLM, TTS, STT capabilities."""

import asyncio
import io
import os
import tempfile
import time
from typing import Any, Dict, List, Optional, Set

from ..breadcrumbs import add_info, SDKLayer
from ..config import ProviderConfig
from ..exceptions import ProviderError
from ..models import AudioFormat, Capability, RawAudioResponse
from ..models.usage import TokenUsage, AudioUsage, UsageBreadcrumb
from ..utils.cost_calculator import get_cost_calculator
from .base import BaseAdapter


class OpenAIAdapter(BaseAdapter):
    """
    OpenAI adapter with text completion, TTS, and STT support.

    Capabilities:
        - TEXT: Chat completions (gpt-4o, gpt-4o-mini, etc.)
        - TTS: Text-to-speech (tts-1, tts-1-hd)
        - STT: Speech-to-text/transcription (whisper-1, gpt-4o-transcribe)

    Diarization:
        - gpt-4o-transcribe-diarize model supports speaker diarization
        - Up to 4 speakers with optional reference audio samples
    """

    name = "openai"

    # Default models for each capability
    DEFAULT_MODELS = {
        "text": "gpt-4o-mini",
        "tts": "tts-1",
        "stt": "whisper-1",
        "diarize": "gpt-4o-transcribe-diarize",
    }

    # TTS voices
    TTS_VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

    def __init__(self, api_key: str, config: Optional[ProviderConfig] = None) -> None:
        super().__init__(api_key, config)
        self._client = None

    @property
    def capabilities(self) -> Set[Capability]:
        return {Capability.TEXT, Capability.TTS, Capability.STT}

    def _init_client(self) -> Any:
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            return OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai package required: pip install openai")

    @property
    def client(self):
        if self._client is None:
            self._client = self._init_client()
        return self._client

    async def complete(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Generate text with OpenAI LLM."""
        model = model or self.DEFAULT_MODELS["text"]
        self._breadcrumb_call_start("complete", model, message_count=len(messages))

        try:
            api_kwargs: Dict[str, Any] = {"model": model, "messages": messages}

            if kwargs.get("temperature") is not None:
                api_kwargs["temperature"] = kwargs["temperature"]
            if kwargs.get("max_tokens") is not None:
                api_kwargs["max_tokens"] = kwargs["max_tokens"]
            if kwargs.get("top_p") is not None:
                api_kwargs["top_p"] = kwargs["top_p"]
            if kwargs.get("stop") is not None:
                api_kwargs["stop"] = kwargs["stop"]
            if kwargs.get("response_format") is not None:
                api_kwargs["response_format"] = kwargs["response_format"]

            response = self.client.chat.completions.create(**api_kwargs)

            content = response.choices[0].message.content or ""
            finish_reason = response.choices[0].finish_reason

            self._breadcrumb_call_success("complete", model, {
                "content_length": len(content),
                "finish_reason": finish_reason,
            })

            return {
                "content": content,
                "finish_reason": finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                }
            }

        except Exception as e:
            self._breadcrumb_call_error("complete", model, e)
            raise ProviderError(f"OpenAI completion failed: {e}", self.name, model)

    async def tts(
        self,
        text: str,
        model: str,
        voice: str,
        **kwargs: Any,
    ) -> RawAudioResponse:
        """
        Convert text to speech using OpenAI TTS.

        Args:
            text: Text to convert (max 4096 chars)
            model: "tts-1" (fast) or "tts-1-hd" (high quality)
            voice: One of: alloy, echo, fable, onyx, nova, shimmer
            **kwargs: Additional parameters:
                - speed: 0.25 to 4.0 (default 1.0)
                - response_format: mp3, opus, aac, flac, wav, pcm

        Returns:
            RawAudioResponse with audio data
        """
        model = model or self.DEFAULT_MODELS["tts"]
        voice = voice or "alloy"

        self._breadcrumb_call_start("tts", model, text_length=len(text), voice=voice)
        start_time = time.time()

        try:
            response_format = kwargs.get("response_format", "mp3")
            speed = kwargs.get("speed", 1.0)

            response = await asyncio.to_thread(
                self.client.audio.speech.create,
                model=model,
                voice=voice,
                input=text,
                response_format=response_format,
                speed=speed,
            )

            audio_data = response.content
            latency_ms = int((time.time() - start_time) * 1000)

            # Map response format to AudioFormat
            format_map = {
                "mp3": AudioFormat.MP3,
                "opus": AudioFormat.OPUS,
                "aac": AudioFormat.MP3,  # Fallback
                "flac": AudioFormat.FLAC,
                "wav": AudioFormat.WAV,
                "pcm": AudioFormat.PCM,
            }
            audio_format = format_map.get(response_format, AudioFormat.MP3)

            # Add usage breadcrumb with cost calculation
            cost = get_cost_calculator().calculate_tts_cost("openai", model, len(text))
            usage_bc = UsageBreadcrumb(
                provider="openai",
                model=model,
                service="tts",
                audio=AudioUsage(characters_processed=len(text)),
                cost=cost,
            )
            add_info(
                layer=SDKLayer.ADAPTER.value,
                action="api_usage",
                message=f"OpenAI TTS: {len(text)} chars, ${cost.total_cost:.6f}",
                **usage_bc.to_breadcrumb_dict(),
            )

            self._breadcrumb_call_success("tts", model, {
                "latency_ms": latency_ms,
                "audio_bytes": len(audio_data),
                "characters": len(text),
                "voice": voice,
            })

            return RawAudioResponse(
                data=audio_data,
                format=audio_format,
                sample_rate=24000,  # OpenAI TTS default
            )

        except Exception as e:
            self._breadcrumb_call_error("tts", model, e)
            raise ProviderError(f"OpenAI TTS failed: {e}", self.name, model)

    async def transcribe(
        self,
        audio: bytes,
        model: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text using OpenAI Whisper.

        Args:
            audio: Audio data bytes
            model: "whisper-1" or "gpt-4o-transcribe" or "gpt-4o-mini-transcribe"
            **kwargs: Additional parameters:
                - language: ISO-639-1 language code (optional)
                - response_format: json, text, srt, verbose_json, vtt
                - timestamp_granularities: ["word", "segment"] for verbose_json
                - prompt: Guide transcription style

        Returns:
            Dict with transcription result:
                - text: Transcribed text
                - language: Detected language
                - duration_seconds: Audio duration in seconds
                - segments: Word/segment timestamps (if verbose_json)
        """
        model = model or self.DEFAULT_MODELS["stt"]
        self._breadcrumb_call_start("stt", model, audio_size=len(audio))
        start_time = time.time()

        try:
            # Create temporary file for audio (OpenAI API requires file-like object)
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                f.write(audio)
                audio_path = f.name

            try:
                with open(audio_path, "rb") as f:
                    # Build API kwargs
                    api_kwargs: Dict[str, Any] = {"model": model, "file": f}

                    if kwargs.get("language"):
                        api_kwargs["language"] = kwargs["language"]

                    response_format = kwargs.get("response_format", "verbose_json")
                    api_kwargs["response_format"] = response_format

                    if kwargs.get("prompt"):
                        api_kwargs["prompt"] = kwargs["prompt"]

                    timestamp_granularities = kwargs.get("timestamp_granularities", ["segment"])
                    if response_format == "verbose_json":
                        api_kwargs["timestamp_granularities"] = timestamp_granularities

                    response = await asyncio.to_thread(
                        self.client.audio.transcriptions.create,
                        **api_kwargs,
                    )
            finally:
                os.unlink(audio_path)  # Cleanup temp file

            latency_ms = int((time.time() - start_time) * 1000)

            # Extract duration from response
            duration_seconds = getattr(response, "duration", None)
            duration_ms = int(duration_seconds * 1000) if duration_seconds else 0

            # Handle different response formats
            if hasattr(response, "text"):
                segments = []
                if hasattr(response, "segments") and response.segments:
                    segments = [
                        s.model_dump() if hasattr(s, "model_dump") else dict(s)
                        for s in response.segments
                    ]

                result = {
                    "text": response.text,
                    "language": getattr(response, "language", None),
                    "duration_seconds": duration_seconds,
                    "segments": segments,
                }
                if hasattr(response, "words") and response.words:
                    result["words"] = [
                        w.model_dump() if hasattr(w, "model_dump") else dict(w)
                        for w in response.words
                    ]
            else:
                result = {"text": str(response)}

            # Add usage breadcrumb with cost calculation
            cost = get_cost_calculator().calculate_stt_cost("openai", model, duration_ms)
            usage_bc = UsageBreadcrumb(
                provider="openai",
                model=model,
                service="stt",
                audio=AudioUsage(
                    duration_ms=duration_ms,
                    segments_count=len(result.get("segments", [])),
                ),
                cost=cost,
                provider_usage={
                    "duration": duration_seconds,
                    "language": result.get("language"),
                },
            )
            add_info(
                layer=SDKLayer.ADAPTER.value,
                action="api_usage",
                message=f"OpenAI STT: {duration_ms}ms, ${cost.total_cost:.6f}",
                **usage_bc.to_breadcrumb_dict(),
            )

            self._breadcrumb_call_success("stt", model, {
                "latency_ms": latency_ms,
                "duration_ms": duration_ms,
                "text_length": len(result.get("text", "")),
            })

            return result

        except Exception as e:
            self._breadcrumb_call_error("stt", model, e)
            raise ProviderError(f"OpenAI transcription failed: {e}", self.name, model)

    async def transcribe_with_diarization(
        self,
        audio: bytes,
        model: str = None,
        num_speakers: int = 2,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Transcribe audio with speaker diarization.

        Uses gpt-4o-transcribe model with automatic speaker identification.
        For inputs >30 seconds, VAD is applied automatically.

        Args:
            audio: Audio data bytes
            model: Model to use (default: gpt-4o-transcribe)
            num_speakers: Expected number of speakers (up to 4)
            **kwargs: Additional parameters passed to transcribe()

        Returns:
            Dict with diarized transcription:
                - text: Full transcription
                - language: Detected language
                - duration_seconds: Audio duration
                - speakers: List of unique speaker IDs found
                - segments: List of segments with speaker labels
        """
        model = model or self.DEFAULT_MODELS["diarize"]

        # Note: OpenAI uses same endpoint; diarization is in response for supported models
        # Requires VAD for inputs >30 seconds (handled automatically)
        result = await self.transcribe(
            audio=audio,
            model=model,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
            **kwargs,
        )

        # Extract unique speakers from segments
        segments = result.get("segments", [])
        speakers = list(set(
            s.get("speaker") for s in segments if s.get("speaker")
        ))

        # Transform to unified diarization format
        return {
            "text": result["text"],
            "language": result.get("language"),
            "duration_seconds": result.get("duration_seconds"),
            "speakers": speakers,
            "segments": segments,
        }

    async def health_check(self) -> bool:
        """Test connectivity to OpenAI API."""
        try:
            self.client.models.list()
            return True
        except Exception:
            return False


__all__ = ["OpenAIAdapter"]
