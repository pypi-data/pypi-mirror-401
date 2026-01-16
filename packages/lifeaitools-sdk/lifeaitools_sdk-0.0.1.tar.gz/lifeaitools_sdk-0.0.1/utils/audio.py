"""
Audio format conversion utilities for Unified AI SDK

Provides functions to convert raw PCM audio data to various formats
including WAV (stdlib), MP3, and OGG Opus (requires pydub).
"""
import wave
import io
from typing import Optional


def _ensure_pydub_available():
    """Check if pydub is available, raise helpful error if not."""
    try:
        from pydub import AudioSegment
        return AudioSegment
    except ImportError:
        raise ImportError(
            "pydub is required for MP3/OGG conversion. "
            "Install it with: pip install pydub\n"
            "Note: pydub also requires ffmpeg to be installed on your system."
        )


def pcm_to_wav(
    pcm_data: bytes,
    sample_rate: int = 24000,
    channels: int = 1,
    sample_width: int = 2
) -> bytes:
    """
    Convert raw PCM audio data to WAV format.

    Uses Python stdlib wave module - no external dependencies.

    Args:
        pcm_data: Raw PCM audio bytes
        sample_rate: Sample rate in Hz (default: 24000 for OpenAI TTS)
        channels: Number of audio channels (default: 1 mono)
        sample_width: Bytes per sample (default: 2 for 16-bit audio)

    Returns:
        WAV file bytes with proper header
    """
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data)
    return buffer.getvalue()


def pcm_to_mp3(
    pcm_data: bytes,
    sample_rate: int = 24000,
    channels: int = 1,
    bitrate: str = "192k"
) -> bytes:
    """
    Convert raw PCM audio data to MP3 format.

    Requires pydub and ffmpeg installed on system.

    Args:
        pcm_data: Raw PCM audio bytes
        sample_rate: Sample rate in Hz (default: 24000)
        channels: Number of audio channels (default: 1 mono)
        bitrate: MP3 bitrate (default: "192k")

    Returns:
        MP3 file bytes

    Raises:
        ImportError: If pydub is not installed
    """
    AudioSegment = _ensure_pydub_available()

    audio = AudioSegment(
        data=pcm_data,
        sample_width=2,
        frame_rate=sample_rate,
        channels=channels
    )

    buffer = io.BytesIO()
    audio.export(buffer, format="mp3", bitrate=bitrate)
    return buffer.getvalue()


def pcm_to_ogg(
    pcm_data: bytes,
    sample_rate: int = 24000,
    channels: int = 1
) -> bytes:
    """
    Convert raw PCM audio data to OGG Opus format.

    Ideal for Telegram voice messages. Requires pydub and ffmpeg
    with libopus codec support.

    Args:
        pcm_data: Raw PCM audio bytes
        sample_rate: Sample rate in Hz (default: 24000)
        channels: Number of audio channels (default: 1 mono)

    Returns:
        OGG Opus file bytes

    Raises:
        ImportError: If pydub is not installed
    """
    AudioSegment = _ensure_pydub_available()

    audio = AudioSegment(
        data=pcm_data,
        sample_width=2,
        frame_rate=sample_rate,
        channels=channels
    )

    buffer = io.BytesIO()
    audio.export(buffer, format="ogg", codec="libopus")
    return buffer.getvalue()


def normalize_sample_rate(
    audio_data: bytes,
    from_rate: int,
    to_rate: int,
    format: str = "pcm"
) -> bytes:
    """
    Resample audio from one sample rate to another.

    Args:
        audio_data: Audio bytes (PCM or WAV format)
        from_rate: Original sample rate in Hz
        to_rate: Target sample rate in Hz
        format: Input format - "pcm" or "wav" (default: "pcm")

    Returns:
        Resampled audio bytes in same format

    Raises:
        ImportError: If pydub is not installed
        ValueError: If format is not supported
    """
    if from_rate == to_rate:
        return audio_data

    AudioSegment = _ensure_pydub_available()

    if format == "pcm":
        audio = AudioSegment(
            data=audio_data,
            sample_width=2,
            frame_rate=from_rate,
            channels=1
        )
    elif format == "wav":
        buffer = io.BytesIO(audio_data)
        audio = AudioSegment.from_wav(buffer)
    else:
        raise ValueError(f"Unsupported format: {format}. Use 'pcm' or 'wav'")

    resampled = audio.set_frame_rate(to_rate)

    if format == "pcm":
        return resampled.raw_data
    else:
        buffer = io.BytesIO()
        resampled.export(buffer, format="wav")
        return buffer.getvalue()


def get_audio_duration_ms(
    audio_data: bytes,
    format: str,
    sample_rate: Optional[int] = None
) -> float:
    """
    Calculate audio duration in milliseconds.

    Args:
        audio_data: Audio bytes
        format: Audio format - "pcm", "wav", or "mp3"
        sample_rate: Required for PCM format (Hz)

    Returns:
        Duration in milliseconds

    Raises:
        ValueError: If format is unsupported or sample_rate missing for PCM
        ImportError: If pydub is not installed (for MP3)
    """
    if format == "pcm":
        if sample_rate is None:
            raise ValueError("sample_rate is required for PCM format")
        sample_width = 2
        channels = 1
        bytes_per_second = sample_rate * sample_width * channels
        return (len(audio_data) / bytes_per_second) * 1000.0

    elif format == "wav":
        buffer = io.BytesIO(audio_data)
        with wave.open(buffer, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return (frames / rate) * 1000.0

    elif format == "mp3":
        AudioSegment = _ensure_pydub_available()
        buffer = io.BytesIO(audio_data)
        audio = AudioSegment.from_mp3(buffer)
        return len(audio)

    else:
        raise ValueError(f"Unsupported format: {format}. Use 'pcm', 'wav', or 'mp3'")


def convert_audio(
    pcm_data: bytes,
    output_format: str,
    sample_rate: int = 24000
) -> bytes:
    """
    Universal audio converter - routes to appropriate conversion function.

    Args:
        pcm_data: Raw PCM audio bytes
        output_format: Target format - "wav", "mp3", "ogg", or "pcm"
        sample_rate: Sample rate in Hz (default: 24000)

    Returns:
        Converted audio bytes

    Raises:
        ValueError: If output_format is not supported
    """
    format_lower = output_format.lower()

    # Normalize format - strip quality suffixes like "mp3_44100_128"
    base_format = format_lower.split("_")[0] if "_" in format_lower else format_lower

    if base_format == "pcm":
        return pcm_data
    elif base_format == "wav":
        return pcm_to_wav(pcm_data, sample_rate=sample_rate)
    elif base_format == "mp3":
        return pcm_to_mp3(pcm_data, sample_rate=sample_rate)
    elif base_format == "ogg":
        return pcm_to_ogg(pcm_data, sample_rate=sample_rate)
    else:
        raise ValueError(
            f"Unsupported output format: {output_format}. "
            f"Supported formats: wav, mp3, ogg, pcm"
        )
