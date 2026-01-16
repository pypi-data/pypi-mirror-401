"""
Clients module for Unified AI SDK.

Provides high-level capability clients that manage provider selection,
fallback logic, and breadcrumb tracking.

Available Clients:
    - AdapterRegistry: Registry for managing provider adapters
    - BaseCapabilityClient: Abstract base class for capability clients
    - UnifiedTTSClient: TTS with multi-provider fallback
    - UnifiedSTTClient: STT with multi-provider fallback
    - UnifiedTextClient: LLM text generation with JSON mode and streaming

Future Clients (to be implemented):
    - UnifiedEmbedClient: Text embeddings
"""

from .base import AdapterRegistry, BaseCapabilityClient
from .stt import UnifiedSTTClient
from .text import UnifiedTextClient
from .tts import UnifiedTTSClient

__all__ = [
    "AdapterRegistry",
    "BaseCapabilityClient",
    "UnifiedSTTClient",
    "UnifiedTextClient",
    "UnifiedTTSClient",
]
