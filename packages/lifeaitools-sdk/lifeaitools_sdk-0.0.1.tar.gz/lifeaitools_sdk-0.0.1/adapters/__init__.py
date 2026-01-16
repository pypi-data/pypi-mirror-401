"""
Adapters module for Unified AI SDK.

Provider-specific adapters that implement the BaseAdapter interface.
Each adapter wraps a provider's SDK and provides a unified interface
for the capabilities it supports.

Available Adapters:
    - BaseAdapter: Abstract base class for all adapters
    - ElevenLabsAdapter: TTS, STT via ElevenLabs
    - GeminiAdapter: TTS, Embed, Text, Vision via Google Gemini
    - OpenAIAdapter: TTS, STT, Text via OpenAI
    - AnthropicAdapter: Text via Anthropic Claude
    - OpenRouterAdapter: Text via OpenRouter (400+ models)

Capability Matrix:
    | Provider   | TEXT | TTS | STT | EMBED | IMAGE | VISION |
    |------------|------|-----|-----|-------|-------|--------|
    | OpenAI     |  ✓   |  ✓  |  ✓  |   -   |   -   |   -    |
    | Anthropic  |  ✓   |  -  |  -  |   -   |   -   |   -    |
    | Gemini     |  ✓   |  ✓  |  -  |   ✓   |   -   |   ✓    |
    | ElevenLabs |  -   |  ✓  |  ✓  |   -   |   -   |   -    |
    | OpenRouter |  ✓   |  -  |  -  |   -   |   -   |   -    |

Diarization Support:
    - OpenAI: gpt-4o-transcribe-diarize (up to 4 speakers)
    - ElevenLabs: Multichannel STT (up to 5 channels)
"""

from .base import BaseAdapter
from .elevenlabs import ElevenLabsAdapter
from .gemini import GeminiAdapter
from .openai import OpenAIAdapter
from .anthropic import AnthropicAdapter
from .openrouter import OpenRouterAdapter

__all__ = [
    "BaseAdapter",
    "ElevenLabsAdapter",
    "GeminiAdapter",
    "OpenAIAdapter",
    "AnthropicAdapter",
    "OpenRouterAdapter",
]
