"""
Gemini adapter for Unified AI SDK.

Provides TTS, Text, STT, Embed, and Vision capabilities via Google's Gemini API.
TTS returns raw PCM audio at 24kHz which is converted to the requested format.
"""

from typing import Any, Dict, List, Optional, Set

from ..breadcrumbs import add_info, SDKLayer
from ..config import ProviderConfig
from ..exceptions import ProviderError
from ..models import AudioFormat, Capability, RawAudioResponse, VoiceInfo
from ..utils.audio import convert_audio
from .base import BaseAdapter


class GeminiAdapter(BaseAdapter):
    """
    Google Gemini adapter with TTS support.

    Gemini TTS returns raw PCM audio at 24000 Hz, mono, 16-bit.
    This adapter handles conversion to MP3, WAV, OGG as needed.

    Prebuilt voices:
        30 voices available including Aoede, Charon, Fenrir, Kore, Puck
        (used in production) and many more.

    Example:
        adapter = GeminiAdapter(api_key="your-key")
        response = await adapter.tts(
            text="Hello world",
            model="gemini-2.5-flash-preview-tts",
            voice="Puck",
            output_format="mp3"
        )
    """

    name = "gemini"

    # Gemini prebuilt voices (30 total)
    # Production voices at top, then alphabetical
    VOICES = [
        # Production favorites
        "Aoede",
        "Charon",
        "Enceladus",
        "Fenrir",
        "Kore",
        "Puck",
        # Other voices (alphabetical)
        "Achernar",
        "Achird",
        "Algenib",
        "Algieba",
        "Alnilam",
        "Auva",
        "Callirrhoe",
        "Despina",
        "Erinome",
        "Gacrux",
        "Helios",
        "Isonoe",
        "Keid",
        "Laomedeia",
        "Leda",
        "Orus",
        "Pegasus",
        "Perseus",
        "Rasalgethi",
        "Sadachbia",
        "Schedar",
        "Sulafat",
        "Vindemiatrix",
        "Zephyr",
        "Zubenelgenubi",
    ]

    # Gemini TTS output parameters (fixed by API)
    SAMPLE_RATE = 24000  # Hz
    CHANNELS = 1  # mono
    SAMPLE_WIDTH = 2  # 16-bit

    def __init__(
        self,
        api_key: str,
        config: Optional[ProviderConfig] = None,
    ) -> None:
        """
        Initialize Gemini adapter.

        Args:
            api_key: Google Gemini API key
            config: Optional provider configuration
        """
        super().__init__(api_key, config)
        self._genai_module = None
        self._types_module = None

    @property
    def capabilities(self) -> Set[Capability]:
        """Gemini supports text, TTS, STT, embeddings, and vision."""
        return {
            Capability.TEXT,
            Capability.TTS,
            Capability.STT,
            Capability.EMBED,
            Capability.VISION,
        }

    def _init_client(self) -> Any:
        """
        Initialize google-genai client.

        Returns:
            Configured genai.Client instance

        Raises:
            ImportError: If google-genai package is not installed
        """
        try:
            from google import genai
            from google.genai import types

            self._genai_module = genai
            self._types_module = types

            client = genai.Client(api_key=self.api_key)
            return client
        except ImportError:
            raise ImportError(
                "google-genai package is required for Gemini adapter. "
                "Install it with: pip install google-genai"
            )

    @property
    def types(self) -> Any:
        """Access to google.genai.types module (lazy loaded)."""
        if self._types_module is None:
            _ = self.client  # Initialize client which loads types
        return self._types_module

    async def tts(
        self,
        text: str,
        model: str,
        voice: str,
        **kwargs: Any,
    ) -> RawAudioResponse:
        """
        Convert text to speech using Gemini API.

        Gemini returns raw PCM audio which is converted to the requested format.

        Args:
            text: Text to convert to speech
            model: Gemini model (e.g., "gemini-2.5-flash-preview-tts")
            voice: Voice name from VOICES list (e.g., "Puck", "Aoede")
            **kwargs:
                output_format: Target format - "mp3", "wav", "ogg", "pcm"
                               Default: "mp3"

        Returns:
            RawAudioResponse with converted audio data

        Raises:
            ProviderError: If API call fails
        """
        self._breadcrumb_call_start("tts", model, text_length=len(text), voice=voice)

        try:
            # Get output format from kwargs
            output_format = kwargs.get("output_format", "mp3")
            if isinstance(output_format, AudioFormat):
                output_format = output_format.value

            # Temperature controls expressiveness (higher = more varied)
            # Default 1.0, reference uses 1.35 for warm/friendly tone
            temperature = kwargs.get("temperature", 1.0)

            # Build TTS config
            config = self.types.GenerateContentConfig(
                temperature=temperature,
                response_modalities=["AUDIO"],
                speech_config=self.types.SpeechConfig(
                    voice_config=self.types.VoiceConfig(
                        prebuilt_voice_config=self.types.PrebuiltVoiceConfig(
                            voice_name=voice,
                        )
                    ),
                ),
            )

            # Streaming mode for long content, batch for short
            streaming = kwargs.get("streaming", False)

            # Call Gemini API
            # Note: SSML breaks like <break time="1.0s"/> are already in text from LLM
            if streaming:
                # Streaming mode - collect chunks
                pcm_chunks = []
                for chunk in self.client.models.generate_content_stream(
                    model=model,
                    contents=text,
                    config=config,
                ):
                    if (chunk.candidates and
                        chunk.candidates[0].content and
                        chunk.candidates[0].content.parts and
                        chunk.candidates[0].content.parts[0].inline_data and
                        chunk.candidates[0].content.parts[0].inline_data.data):
                        pcm_chunks.append(chunk.candidates[0].content.parts[0].inline_data.data)
                pcm_data = b"".join(pcm_chunks)
            else:
                # Batch mode - single request/response
                response = self.client.models.generate_content(
                    model=model,
                    contents=text,
                    config=config,
                )
                pcm_data = response.candidates[0].content.parts[0].inline_data.data

            # Add breadcrumb for format conversion
            add_info(
                layer=SDKLayer.ADAPTER.value,
                action="audio_format_conversion",
                message=f"Converting PCM to {output_format}",
                from_format="pcm",
                to_format=output_format,
                pcm_bytes=len(pcm_data),
                sample_rate=self.SAMPLE_RATE,
            )

            # Convert PCM to requested format
            audio_data = convert_audio(
                pcm_data=pcm_data,
                output_format=output_format,
                sample_rate=self.SAMPLE_RATE,
            )

            # Success breadcrumb
            self._breadcrumb_call_success(
                "tts",
                model,
                {
                    "pcm_bytes": len(pcm_data),
                    "output_bytes": len(audio_data),
                    "output_format": output_format,
                    "voice": voice,
                },
            )

            # Resolve AudioFormat enum
            try:
                audio_format_enum = AudioFormat(output_format)
            except ValueError:
                audio_format_enum = AudioFormat.MP3

            return RawAudioResponse(
                data=audio_data,
                format=audio_format_enum,
                sample_rate=self.SAMPLE_RATE,
                channels=self.CHANNELS,
            )

        except Exception as e:
            self._breadcrumb_call_error(
                "tts",
                model,
                e,
                recommendations=[
                    "Check Gemini API key validity",
                    "Verify voice name is valid",
                    "Check model supports TTS (gemini-2.5-flash-preview-tts)",
                ],
            )
            raise ProviderError(
                message=f"Gemini TTS failed: {e}",
                provider=self.name,
                model=model,
            )

    async def get_voices(self) -> List[VoiceInfo]:
        """
        Get list of available Gemini voices.

        Returns:
            List of VoiceInfo objects for all 30 prebuilt voices
        """
        return [
            VoiceInfo(
                id=voice,
                name=voice,
                provider=self.name,
                language_codes=["en-US"],  # Gemini voices are primarily English
                description=f"Gemini prebuilt voice: {voice}",
            )
            for voice in self.VOICES
        ]

    async def complete(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Generate text with Gemini LLM.

        Args:
            messages: Chat messages [{"role": "user", "content": "..."}]
            model: Gemini model name (e.g., "gemini-2.0-flash")
            **kwargs: temperature, max_tokens, top_p, stop, response_format

        Returns:
            Dict with content, finish_reason, usage
        """
        self._breadcrumb_call_start("complete", model, message_count=len(messages))

        try:
            # Build generation config from kwargs - NO hardcoding, use defaults only if not provided
            temperature = kwargs.get("temperature")
            max_tokens = kwargs.get("max_tokens")
            top_p = kwargs.get("top_p")
            stop = kwargs.get("stop")
            response_format = kwargs.get("response_format")

            # Build config dict, only include non-None values
            config_dict: Dict[str, Any] = {}
            if temperature is not None:
                config_dict["temperature"] = temperature
            if max_tokens is not None:
                config_dict["max_output_tokens"] = max_tokens
            if top_p is not None:
                config_dict["top_p"] = top_p
            if stop is not None:
                config_dict["stop_sequences"] = stop

            # Map response_format to Gemini's response_mime_type
            # {"type": "json_object"} -> "application/json"
            if response_format:
                fmt_type = response_format.get("type", "")
                if fmt_type == "json_object":
                    config_dict["response_mime_type"] = "application/json"
                elif fmt_type == "json_schema":
                    config_dict["response_mime_type"] = "application/json"
                    # If schema provided, pass it
                    if "json_schema" in response_format:
                        config_dict["response_schema"] = response_format["json_schema"]

            # Convert messages to Gemini format
            contents = self._convert_messages_to_gemini(messages)

            # Build config object
            config = self.types.GenerateContentConfig(**config_dict) if config_dict else None

            # Call Gemini API
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )

            content = response.text if response.text else ""
            finish_reason = None
            if response.candidates and response.candidates[0].finish_reason:
                finish_reason = str(response.candidates[0].finish_reason)

            # Extract usage
            usage = {}
            if hasattr(response, "usage_metadata") and response.usage_metadata:
                usage = {
                    "prompt_tokens": getattr(response.usage_metadata, "prompt_token_count", 0),
                    "completion_tokens": getattr(response.usage_metadata, "candidates_token_count", 0),
                    "total_tokens": getattr(response.usage_metadata, "total_token_count", 0),
                }

            self._breadcrumb_call_success("complete", model, {
                "content_length": len(content),
                "finish_reason": finish_reason,
            })

            return {
                "content": content,
                "finish_reason": finish_reason or "stop",
                "usage": usage,
            }

        except Exception as e:
            self._breadcrumb_call_error(
                "complete",
                model,
                e,
                recommendations=[
                    "Check Gemini API key validity",
                    "Verify model supports text generation",
                    "Check response_format is valid",
                ],
            )
            raise ProviderError(
                message=f"Gemini completion failed: {e}",
                provider=self.name,
                model=model,
            )

    def _convert_messages_to_gemini(self, messages: List[Dict[str, Any]]) -> List:
        """Convert OpenAI-style messages to Gemini Contents format."""
        contents = []
        system_prompt = None

        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            if role == "system":
                system_prompt = content
            elif role == "user":
                contents.append(self.types.Content(
                    role="user",
                    parts=[self.types.Part(text=content)]
                ))
            elif role == "assistant":
                contents.append(self.types.Content(
                    role="model",
                    parts=[self.types.Part(text=content)]
                ))

        # Prepend system prompt to first user message if exists
        if system_prompt and contents:
            first_text = contents[0].parts[0].text
            contents[0] = self.types.Content(
                role="user",
                parts=[self.types.Part(text=f"{system_prompt}\n\n{first_text}")]
            )

        return contents
