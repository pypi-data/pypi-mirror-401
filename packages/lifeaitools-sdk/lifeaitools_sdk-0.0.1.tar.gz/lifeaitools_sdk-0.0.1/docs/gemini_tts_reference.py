"""
Gemini TTS Reference Implementation
Source: Google AI Studio export
Date: 2026-01-13

Key Settings:
- Model: gemini-2.5-pro-preview-tts (Pro model for higher quality)
- Voice: Enceladus (one of 30 prebuilt voices)
- Temperature: 1.35 (higher = more expressive/varied)
- Streaming: Uses generate_content_stream for chunked output
- Output: Raw PCM audio (L16, 24000Hz, mono)

Available Models:
- gemini-2.5-pro-preview-tts (higher quality, slower)
- gemini-2.5-flash-preview-tts (faster, good quality)

Available Voices (30 total):
Production favorites: Aoede, Charon, Fenrir, Kore, Puck, Enceladus
Others: Achernar, Achird, Algenib, Algieba, Alnilam, Auva, Callirrhoe,
        Despina, Erinome, Gacrux, Helios, Isonoe, Keid, Laomedeia,
        Leda, Orus, Pegasus, Perseus, Rasalgethi, Sadachbia, Schedar,
        Sulafat, Vindemiatrix, Zephyr, Zubenelgenubi

SSML-like breaks supported: <break time="1.0s"/>
"""

import base64
import mimetypes
import os
import struct
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to: {file_name}")


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.5-pro-preview-tts"

    # Content structure - use types.Content with role="user"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Read aloud in a warm and friendly tone as experienced business trainer:
'Your text here with optional SSML breaks like <break time="1.0s"/>'"""),
            ],
        ),
    ]

    # Key config: temperature controls expressiveness
    generate_content_config = types.GenerateContentConfig(
        temperature=1.35,  # Higher = more expressive/varied speech
        response_modalities=["audio"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name="Enceladus"  # Choose from 30 voices
                )
            )
        ),
    )

    # Streaming for chunked audio output
    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"output_chunk_{file_index}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            if file_extension is None:
                file_extension = ".wav"
                data_buffer = convert_to_wav(inline_data.data, inline_data.mime_type)
            save_binary_file(f"{file_name}{file_extension}", data_buffer)
        else:
            print(chunk.text)


def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    """Generates a WAV file header for raw PCM audio data.

    Gemini TTS returns raw PCM: L16 (16-bit), 24000Hz, mono
    """
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF",          # ChunkID
        chunk_size,       # ChunkSize
        b"WAVE",          # Format
        b"fmt ",          # Subchunk1ID
        16,               # Subchunk1Size (PCM)
        1,                # AudioFormat (PCM)
        num_channels,     # NumChannels
        sample_rate,      # SampleRate
        byte_rate,        # ByteRate
        block_align,      # BlockAlign
        bits_per_sample,  # BitsPerSample
        b"data",          # Subchunk2ID
        data_size         # Subchunk2Size
    )
    return header + audio_data


def parse_audio_mime_type(mime_type: str) -> dict[str, int]:
    """Parse audio params from MIME type like 'audio/L16;rate=24000'"""
    bits_per_sample = 16
    rate = 24000

    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate = int(param.split("=", 1)[1])
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass

    return {"bits_per_sample": bits_per_sample, "rate": rate}


if __name__ == "__main__":
    generate()
