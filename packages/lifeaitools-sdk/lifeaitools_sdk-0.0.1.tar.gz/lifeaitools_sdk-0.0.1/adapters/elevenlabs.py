"""
ElevenLabs Adapter for Unified AI SDK.

Provides TTS capabilities via ElevenLabs API with:
- Safe retry strategy (no retries on quota/auth errors)
- Breadcrumb integration for debugging
- Streaming support
- Voice listing and quota checking

Ported from: services/tts/elevenlabs_client.py
"""
import asyncio
import time
from typing import Any, AsyncIterator, Dict, List, Optional, Set

import aiohttp

from ..breadcrumbs import add_info, add_warning, SDKLayer
from ..models.usage import AudioUsage, CostBreakdown, UsageBreadcrumb
from ..utils.cost_calculator import get_cost_calculator
from ..config import ProviderConfig
from ..exceptions import ProviderError, QuotaExceededError, RateLimitError
from ..models import AudioFormat, Capability, RawAudioResponse, VoiceInfo
from ..utils.retry import SafeRetryStrategy
from .base import BaseAdapter


class ElevenLabsAdapter(BaseAdapter):
    """
    ElevenLabs TTS adapter with safe retry logic.

    Features:
        - Text-to-speech generation
        - Streaming TTS
        - Voice listing
        - Quota checking
        - Safe retry strategy (no retries on 402/quota errors)

    Example:
        adapter = ElevenLabsAdapter(api_key="xi-...")
        response = await adapter.tts(
            text="Hello world",
            model="eleven_multilingual_v2",
            voice="21m00Tcm4TlvDq8ikWAM"
        )
    """

    name: str = "elevenlabs"
    API_ENDPOINT: str = "https://api.elevenlabs.io/v1"

    def __init__(
        self,
        api_key: str,
        config: Optional[ProviderConfig] = None,
    ) -> None:
        """
        Initialize ElevenLabs adapter.

        Args:
            api_key: ElevenLabs API key (xi-...)
            config: Optional provider configuration
        """
        super().__init__(api_key, config)
        self._retry_strategy = SafeRetryStrategy()
        self._session: Optional[aiohttp.ClientSession] = None

    @property
    def capabilities(self) -> Set[Capability]:
        """ElevenLabs supports TTS and STT capabilities."""
        return {Capability.TTS, Capability.STT}

    def _init_client(self) -> Dict[str, str]:
        """
        Initialize client headers for API requests.

        Returns:
            Headers dict with API key
        """
        return {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg",
        }

    async def _get_session(self) -> aiohttp.ClientSession:
        """
        Get or create aiohttp session.

        Returns:
            Active aiohttp ClientSession
        """
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(
                total=self.config.timeout_seconds if self.config else 60.0
            )
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def tts(
        self,
        text: str,
        model: str,
        voice: str,
        **kwargs: Any,
    ) -> RawAudioResponse:
        """
        Convert text to speech.

        Args:
            text: Text to convert
            model: Model ID (e.g., "eleven_multilingual_v2")
            voice: Voice ID (e.g., "21m00Tcm4TlvDq8ikWAM")
            **kwargs: Additional parameters:
                - voice_settings: Dict with stability, similarity_boost, etc.
                - output_format: Audio format (default: mp3_44100_128)
                - max_retries: Override default retry count (default: 3)

        Returns:
            RawAudioResponse with audio data

        Raises:
            RateLimitError: If rate limited (retryable)
            QuotaExceededError: If quota exhausted (not retryable)
            ProviderError: For other API errors
        """
        self._breadcrumb_call_start("tts", model, text_length=len(text), voice=voice)

        start_time = time.time()
        attempt = 0
        max_retries = kwargs.get("max_retries", 3)

        voice_settings = kwargs.get("voice_settings", {
            "stability": 0.5,
            "similarity_boost": 0.75,
        })

        url = f"{self.API_ENDPOINT}/text-to-speech/{voice}"
        request_body = {
            "text": text,
            "model_id": model,
            "voice_settings": voice_settings,
        }

        output_format = kwargs.get("output_format", "mp3_44100_128")
        if output_format:
            url = f"{url}?output_format={output_format}"

        session = await self._get_session()
        headers = self._init_client()

        while attempt < max_retries:
            try:
                async with session.post(
                    url,
                    headers=headers,
                    json=request_body,
                ) as response:
                    if response.status == 200:
                        audio_data = await response.read()
                        latency_ms = (time.time() - start_time) * 1000

                        self._breadcrumb_call_success("tts", model, {
                            "latency_ms": latency_ms,
                            "audio_bytes": len(audio_data),
                            "attempts": attempt + 1,
                            "voice": voice,
                        })

                        return RawAudioResponse(
                            data=audio_data,
                            format=AudioFormat.MP3,
                            sample_rate=44100,
                        )

                    error_text = await response.text()
                    await self._handle_error_response(
                        response.status,
                        error_text,
                        model,
                        attempt,
                        max_retries,
                    )

            except (RateLimitError, QuotaExceededError, ProviderError):
                raise
            except aiohttp.ClientError as e:
                self._breadcrumb_call_error(
                    "tts", model, e,
                    recommendations=["Check network connectivity"],
                    retry_strategy={"is_retryable": True},
                )
                if attempt >= max_retries - 1:
                    raise ProviderError(
                        message=f"Network error: {e}",
                        provider=self.name,
                        model=model,
                    )

            should_retry, wait_seconds = self._retry_strategy.should_retry(
                429, attempt, max_retries
            )
            if should_retry:
                add_warning(
                    layer=SDKLayer.RETRY.value,
                    action="retry_scheduled",
                    message=f"Retrying after {wait_seconds}s (attempt {attempt + 1}/{max_retries})",
                    provider=self.name,
                    attempt=attempt + 1,
                    wait_seconds=wait_seconds,
                )
                await asyncio.sleep(wait_seconds)
            attempt += 1

        raise ProviderError(
            message="Max retries exceeded",
            provider=self.name,
            model=model,
        )

    async def _handle_error_response(
        self,
        status_code: int,
        error_text: str,
        model: str,
        attempt: int,
        max_retries: int,
    ) -> None:
        """
        Handle error responses from ElevenLabs API.

        Args:
            status_code: HTTP status code
            error_text: Error response body
            model: Model being used
            attempt: Current attempt number
            max_retries: Maximum retries allowed

        Raises:
            RateLimitError: On 429 status
            QuotaExceededError: On 402 status
            ProviderError: On other errors
        """
        if status_code == 429:
            retry_after = 10
            error = RateLimitError(
                message=f"Rate limited: {error_text}",
                provider=self.name,
                model=model,
                http_status=status_code,
                retry_after_seconds=retry_after,
            )
            add_warning(
                layer=SDKLayer.RETRY.value,
                action="rate_limit_hit",
                message=f"Rate limited, waiting {retry_after}s (attempt {attempt + 1}/{max_retries})",
                provider=self.name,
                attempt=attempt + 1,
                wait_seconds=retry_after,
            )
            if attempt >= max_retries - 1:
                self._breadcrumb_call_error(
                    "tts", model, error,
                    recommendations=["Reduce request rate", "Implement backoff"],
                    retry_strategy={"is_retryable": True, "retry_after_seconds": retry_after},
                )
                raise error
            await asyncio.sleep(retry_after)
            return

        if status_code == 402:
            error = QuotaExceededError(
                message=f"Quota exceeded: {error_text}",
                provider=self.name,
                model=model,
                http_status=status_code,
            )
            self._breadcrumb_call_error(
                "tts", model, error,
                recommendations=["Check ElevenLabs quota", "Switch to Gemini TTS"],
                retry_strategy={"is_retryable": False},
            )
            raise error

        should_retry, wait_seconds = self._retry_strategy.should_retry(
            status_code, attempt, max_retries
        )

        if not should_retry:
            error = ProviderError(
                message=f"API error {status_code}: {error_text}",
                provider=self.name,
                model=model,
                http_status=status_code,
            )
            self._breadcrumb_call_error(
                "tts", model, error,
                recommendations=[self._retry_strategy.get_error_message(status_code)],
                retry_strategy={"is_retryable": False},
            )
            raise error

        add_warning(
            layer=SDKLayer.RETRY.value,
            action="retry_scheduled",
            message=f"Error {status_code}, retrying after {wait_seconds}s",
            provider=self.name,
            attempt=attempt + 1,
            wait_seconds=wait_seconds,
            status_code=status_code,
        )
        await asyncio.sleep(wait_seconds)

    async def tts_stream(
        self,
        text: str,
        model: str,
        voice: str,
        **kwargs: Any,
    ) -> AsyncIterator[bytes]:
        """
        Stream text-to-speech audio chunks.

        Args:
            text: Text to convert
            model: Model ID
            voice: Voice ID
            **kwargs: Additional parameters (voice_settings, etc.)

        Yields:
            Audio data chunks as they arrive

        Raises:
            RateLimitError: If rate limited
            QuotaExceededError: If quota exhausted
            ProviderError: For other API errors
        """
        self._breadcrumb_call_start(
            "tts_stream", model, text_length=len(text), voice=voice
        )

        voice_settings = kwargs.get("voice_settings", {
            "stability": 0.5,
            "similarity_boost": 0.75,
        })

        url = f"{self.API_ENDPOINT}/text-to-speech/{voice}/stream"
        request_body = {
            "text": text,
            "model_id": model,
            "voice_settings": voice_settings,
        }

        output_format = kwargs.get("output_format", "mp3_44100_128")
        if output_format:
            url = f"{url}?output_format={output_format}"

        session = await self._get_session()
        headers = self._init_client()

        start_time = time.time()
        total_bytes = 0

        async with session.post(
            url,
            headers=headers,
            json=request_body,
        ) as response:
            if response.status != 200:
                error_text = await response.text()
                await self._handle_error_response(
                    response.status, error_text, model, 0, 1
                )

            async for chunk in response.content.iter_chunked(8192):
                total_bytes += len(chunk)
                yield chunk

        latency_ms = (time.time() - start_time) * 1000
        self._breadcrumb_call_success("tts_stream", model, {
            "latency_ms": latency_ms,
            "audio_bytes": total_bytes,
            "voice": voice,
        })

    async def get_voices(self) -> List[VoiceInfo]:
        """
        Get list of available voices.

        Returns:
            List of VoiceInfo objects with voice details

        Raises:
            ProviderError: If API request fails
        """
        url = f"{self.API_ENDPOINT}/voices"
        session = await self._get_session()
        headers = {
            "xi-api-key": self.api_key,
            "Accept": "application/json",
        }

        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                raise ProviderError(
                    message=f"Failed to get voices: {error_text}",
                    provider=self.name,
                    model="",
                    http_status=response.status,
                )

            data = await response.json()
            voices = []
            for voice in data.get("voices", []):
                voices.append(VoiceInfo(
                    id=voice.get("voice_id", ""),
                    name=voice.get("name", ""),
                    provider=self.name,
                    language_codes=voice.get("labels", {}).get("language", "").split(","),
                    gender=voice.get("labels", {}).get("gender"),
                    description=voice.get("description"),
                    preview_url=voice.get("preview_url"),
                ))
            return voices

    async def check_quota(self) -> Dict[str, Any]:
        """
        Check remaining quota/credits.

        Returns:
            Dict with quota information:
                - character_count: Used characters
                - character_limit: Total limit
                - remaining_characters: Remaining characters
                - can_extend_character_limit: Whether limit can be extended
                - next_character_count_reset_unix: Reset timestamp

        Raises:
            ProviderError: If API request fails
        """
        url = f"{self.API_ENDPOINT}/user/subscription"
        session = await self._get_session()
        headers = {
            "xi-api-key": self.api_key,
            "Accept": "application/json",
        }

        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                error_text = await response.text()
                raise ProviderError(
                    message=f"Failed to check quota: {error_text}",
                    provider=self.name,
                    model="",
                    http_status=response.status,
                )

            data = await response.json()
            character_count = data.get("character_count", 0)
            character_limit = data.get("character_limit", 0)

            return {
                "character_count": character_count,
                "character_limit": character_limit,
                "remaining_characters": character_limit - character_count,
                "can_extend_character_limit": data.get("can_extend_character_limit", False),
                "next_character_count_reset_unix": data.get("next_character_count_reset_unix"),
            }

    async def health_check(self) -> bool:
        """
        Test connectivity to ElevenLabs API.

        Returns:
            True if API is reachable and responding
        """
        try:
            quota = await self.check_quota()
            return quota.get("character_limit", 0) > 0
        except Exception:
            return False

    async def transcribe(
        self,
        audio: bytes,
        model: str = "scribe_v1",
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Transcribe audio to text using ElevenLabs Scribe.

        ElevenLabs STT (Scribe v2) supports 90+ languages with high accuracy.

        Args:
            audio: Audio data bytes (supports various formats)
            model: "scribe_v1" (default) or future models
            **kwargs: Additional parameters:
                - language: ISO-639-1 language code (auto-detected if not provided)
                - keyterms: List of up to 100 words/phrases to bias transcription
                - num_speakers: Expected number of speakers (for diarization)
                - multichannel: Enable per-channel speaker assignment (up to 5 channels)

        Returns:
            Dict with transcription result:
                - text: Transcribed text
                - language: Detected/used language
                - duration_seconds: Audio duration
                - segments: List of timestamped segments
                - speakers: Speaker information (if multichannel or diarization)

        Note:
            Billing is per hour of audio. Multichannel STT assigns speaker IDs
            based on channel number, supporting up to 5 channels.
        """
        self._breadcrumb_call_start("transcribe", model, audio_bytes=len(audio))
        start_time = time.time()

        url = f"{self.API_ENDPOINT}/speech-to-text"
        session = await self._get_session()

        try:
            # Prepare form data
            import aiohttp
            form = aiohttp.FormData()
            form.add_field(
                'audio',
                audio,
                filename='audio.mp3',
                content_type='audio/mpeg'
            )

            if kwargs.get("language"):
                form.add_field("language_code", kwargs["language"])
            if kwargs.get("keyterms"):
                form.add_field("keyterms", ",".join(kwargs["keyterms"]))
            if kwargs.get("num_speakers"):
                form.add_field("num_speakers", str(kwargs["num_speakers"]))
            if kwargs.get("multichannel"):
                form.add_field("multichannel", "true")

            headers = {
                "xi-api-key": self.api_key,
                "Accept": "application/json",
            }

            async with session.post(url, headers=headers, data=form) as response:
                if response.status == 200:
                    data = await response.json()
                    latency_ms = (time.time() - start_time) * 1000
                    duration_seconds = data.get("duration_seconds", 0)
                    duration_ms = int(duration_seconds * 1000)

                    result = {
                        "text": data.get("text", ""),
                        "language": data.get("language_code"),
                        "duration_seconds": duration_seconds,
                        "words": data.get("words", []),
                        "speakers": data.get("speakers", []) if kwargs.get("num_speakers") or kwargs.get("multichannel") else [],
                    }

                    # Add usage breadcrumb with cost (ElevenLabs bills per hour)
                    cost = get_cost_calculator().calculate_stt_cost(
                        self.name, model, duration_ms
                    )
                    usage_bc = UsageBreadcrumb(
                        provider=self.name,
                        model=model,
                        service="stt",
                        audio=AudioUsage(
                            duration_ms=duration_ms,
                            segments_count=len(result.get("words", [])),
                        ),
                        cost=cost,
                        provider_usage=data,
                    )
                    add_info(
                        layer=SDKLayer.ADAPTER.value,
                        action="api_usage",
                        message=f"STT completed: {duration_seconds:.1f}s audio",
                        **usage_bc.to_breadcrumb_dict()
                    )

                    self._breadcrumb_call_success("transcribe", model, {
                        "latency_ms": latency_ms,
                        "text_length": len(result["text"]),
                        "language": result.get("language"),
                        "duration_seconds": duration_seconds,
                        "cost_usd": cost.total_cost if cost else 0,
                    })

                    return result

                else:
                    error_text = await response.text()
                    error = ProviderError(
                        message=f"Transcription failed: {error_text}",
                        provider=self.name,
                        model=model,
                        http_status=response.status,
                    )
                    self._breadcrumb_call_error("transcribe", model, error)
                    raise error

        except ProviderError:
            raise
        except Exception as e:
            self._breadcrumb_call_error("transcribe", model, e)
            raise ProviderError(
                message=f"Transcription error: {e}",
                provider=self.name,
                model=model,
            )


__all__ = ["ElevenLabsAdapter"]
