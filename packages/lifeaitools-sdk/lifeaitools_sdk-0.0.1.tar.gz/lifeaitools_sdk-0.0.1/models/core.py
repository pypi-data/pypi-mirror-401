"""
Type definitions for Unified AI SDK.

Contains request/response dataclasses, enums, and type definitions
for all SDK capabilities (TTS, STT, Text, Embed, Image, Vision).

Important: This module is designed to be independent with NO circular imports.
Do not import from breadcrumbs.py or exceptions.py here.
"""

from abc import ABC
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Optional, Union


# === ENUMS ===


class AudioFormat(Enum):
    """Supported audio output formats."""

    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"
    PCM = "pcm"
    FLAC = "flac"
    OPUS = "opus"


class Capability(Enum):
    """SDK capabilities (service types)."""

    TEXT = "text"
    TTS = "tts"
    STT = "stt"
    EMBED = "embed"
    IMAGE = "image"
    VISION = "vision"


# === BASE REQUEST/RESPONSE ===


@dataclass
class BaseRequest(ABC):
    """
    Base request - all capability requests inherit from this.
    Supports dict/JSON serialization and provider-specific extensions.
    """

    model: Optional[str] = None
    timeout: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    include_breadcrumbs: bool = True
    timeout_seconds: Optional[int] = None
    provider_params: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict (for JSON, logging, queuing)."""
        result = {}
        for k, v in asdict(self).items():
            if v is not None:
                if isinstance(v, Enum):
                    result[k] = v.value
                else:
                    result[k] = v
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseRequest":
        """Deserialize from dict/JSON."""
        return cls(**data)

    def merge(self, overrides: Dict[str, Any]) -> "BaseRequest":
        """Create new request with overrides applied."""
        data = self.to_dict()
        data.update(overrides)
        return self.__class__.from_dict(data)


@dataclass
class BaseResponse(ABC):
    """
    Base response - all capability responses inherit from this.

    Contains common fields for tracking success, provider info,
    latency, cost, and debugging information.
    """

    success: bool
    provider: str
    model: str
    latency_ms: float
    cost: Optional[float] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw_response: Optional[Any] = None
    breadcrumbs: Optional[List[Dict[str, Any]]] = None
    execution_warnings: Optional[List[Dict[str, Any]]] = None


# === TTS REQUEST/RESPONSE ===


@dataclass
class TTSRequest(BaseRequest):
    """Request for text-to-speech synthesis."""

    text: str = ""
    voice: str = "default"
    output_format: AudioFormat = AudioFormat.MP3
    speed: float = 1.0
    pitch: float = 1.0
    language: Optional[str] = None
    stream: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dict, converting enums to values."""
        result = super().to_dict()
        if "output_format" in result and isinstance(self.output_format, AudioFormat):
            result["output_format"] = self.output_format.value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TTSRequest":
        """Deserialize from dict, converting string to AudioFormat."""
        if "output_format" in data and isinstance(data["output_format"], str):
            data["output_format"] = AudioFormat(data["output_format"])
        return cls(**data)


@dataclass
class RawAudioResponse:
    """Raw audio data from TTS synthesis."""

    data: bytes
    format: AudioFormat
    sample_rate: int
    channels: int = 1
    duration_ms: Optional[float] = None

    def save(self, path: str) -> None:
        """Save audio data to file."""
        with open(path, "wb") as f:
            f.write(self.data)


@dataclass
class TTSResponse(BaseResponse):
    """Response from TTS synthesis."""

    audio: Optional[RawAudioResponse] = None
    text_length: int = 0
    voice_used: str = ""
    format_requested: AudioFormat = AudioFormat.MP3
    format_actual: AudioFormat = AudioFormat.MP3

    def save(self, path: str) -> None:
        """Save audio to file."""
        if self.audio:
            self.audio.save(path)


# === VOICE INFO ===


@dataclass
class VoiceInfo:
    """Information about an available voice."""

    id: str
    name: str
    provider: str
    language_codes: List[str] = field(default_factory=list)
    gender: Optional[str] = None
    description: Optional[str] = None
    preview_url: Optional[str] = None


# === TEXT REQUEST/RESPONSE ===


@dataclass
class TextRequest(BaseRequest):
    """Request for text generation (LLM)."""

    messages: Optional[List[Dict[str, Any]]] = None
    prompt: Optional[str] = None
    system: Optional[str] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    stop: Optional[List[str]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[Union[str, Dict[str, Any]]] = None
    response_format: Optional[Dict[str, Any]] = None
    stream: bool = False


@dataclass
class TextResponse(BaseResponse):
    """Response from text generation."""

    content: str = ""
    finish_reason: Optional[str] = None
    tool_calls: Optional[List[Dict[str, Any]]] = None
    thinking: Optional[str] = None


# === STT REQUEST/RESPONSE ===


@dataclass
class STTRequest(BaseRequest):
    """Request for speech-to-text (transcription)."""

    audio: Union[str, bytes] = ""
    language: Optional[str] = None
    response_format: str = "json"
    timestamp_granularity: Optional[str] = None


@dataclass
class STTResponse(BaseResponse):
    """Response from transcription."""

    text: str = ""
    language: Optional[str] = None
    duration_seconds: Optional[float] = None
    segments: List[Dict[str, Any]] = field(default_factory=list)
    words: Optional[List[Dict[str, Any]]] = None


# === EMBED REQUEST/RESPONSE ===


@dataclass
class EmbedRequest(BaseRequest):
    """Request for embeddings."""

    texts: List[str] = field(default_factory=list)
    dimensions: Optional[int] = None
    encoding_format: str = "float"


@dataclass
class EmbedResponse(BaseResponse):
    """Response from embeddings."""

    vectors: List[List[float]] = field(default_factory=list)
    dimensions: int = 0


# === IMAGE REQUEST/RESPONSE ===


@dataclass
class ImageRequest(BaseRequest):
    """Request for image generation."""

    prompt: str = ""
    size: str = "1024x1024"
    quality: str = "standard"
    style: Optional[str] = None
    response_format: str = "url"
    n: int = 1


@dataclass
class ImageResponse(BaseResponse):
    """Response from image generation."""

    images: List[str] = field(default_factory=list)
    revised_prompt: Optional[str] = None

    def save(self, path: str, index: int = 0) -> None:
        """Save image to file (placeholder for base64 handling)."""
        pass


# === VISION REQUEST/RESPONSE ===


@dataclass
class VisionRequest(BaseRequest):
    """Request for image understanding."""

    image: Union[str, bytes, List[str]] = ""
    prompt: str = ""
    detail: str = "auto"


@dataclass
class VisionResponse(BaseResponse):
    """Response from vision analysis."""

    content: str = ""
    finish_reason: Optional[str] = None
