"""
Base adapter for provider implementations in Unified AI SDK.

All provider adapters (ElevenLabs, OpenAI, Gemini, etc.) inherit from BaseAdapter.
Includes breadcrumb integration for debugging and observability.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterator, List, Optional, Set

from ..breadcrumbs import add_error, add_info, add_success, SDKLayer
from ..config import ProviderConfig
from ..models import Capability, RawAudioResponse


class BaseAdapter(ABC):
    """
    Base class for provider adapters with breadcrumb integration.

    All provider-specific adapters inherit from this class and implement
    the capability methods they support (tts, transcribe, embed, complete).

    Attributes:
        name: Provider name ("elevenlabs", "openai", "gemini", etc.)
        api_key: API key for the provider
        config: Optional provider-specific configuration
        _client: Lazy-initialized provider SDK client

    Example:
        class ElevenLabsAdapter(BaseAdapter):
            name = "elevenlabs"

            @property
            def capabilities(self) -> Set[Capability]:
                return {Capability.TTS}

            def _init_client(self) -> Any:
                from elevenlabs.client import ElevenLabs
                return ElevenLabs(api_key=self.api_key)

            async def tts(self, text: str, model: str, voice: str, **kwargs):
                # Implementation...
    """

    name: str  # Provider name: "openai", "elevenlabs", "gemini", etc.

    def __init__(
        self,
        api_key: str,
        config: Optional[ProviderConfig] = None,
    ) -> None:
        """
        Initialize base adapter.

        Args:
            api_key: API key for the provider
            config: Optional provider configuration with timeout, retries, etc.
        """
        self.api_key = api_key
        self.config = config
        self._client: Any = None

    @property
    @abstractmethod
    def capabilities(self) -> Set[Capability]:
        """
        Return the set of capabilities this adapter supports.

        Returns:
            Set of Capability enum values (e.g., {Capability.TTS, Capability.STT})
        """
        pass

    @abstractmethod
    def _init_client(self) -> Any:
        """
        Initialize the provider SDK client.

        This method is called lazily when the client is first needed.
        Subclasses must implement this to return their provider's SDK client.

        Returns:
            Provider SDK client instance
        """
        pass

    @property
    def client(self) -> Any:
        """
        Lazy-initialized provider client.

        Returns:
            Provider SDK client, initialized on first access
        """
        if self._client is None:
            self._client = self._init_client()
        return self._client

    def supports(self, capability: Capability) -> bool:
        """
        Check if this adapter supports a given capability.

        Args:
            capability: The capability to check

        Returns:
            True if capability is supported, False otherwise
        """
        return capability in self.capabilities

    async def health_check(self) -> bool:
        """
        Test connectivity to the provider.

        Default implementation attempts to initialize the client.
        Subclasses can override for more sophisticated checks.

        Returns:
            True if provider is reachable and responding
        """
        try:
            _ = self.client
            return True
        except Exception:
            return False

    # --- Breadcrumb Helpers (Protected) ---

    def _breadcrumb_call_start(
        self,
        capability: str,
        model: str,
        **kwargs: Any,
    ) -> None:
        """
        Add breadcrumb when starting provider call.

        Args:
            capability: Capability being invoked (e.g., "tts", "embed")
            model: Model being used
            **kwargs: Additional metadata to include
        """
        add_info(
            layer=SDKLayer.ADAPTER.value,
            action=f"{self.name}_call_start",
            message=f"Calling {self.name} API for {capability}",
            capability=capability,
            provider=self.name,
            model=model,
            metadata=kwargs,
        )

    def _breadcrumb_call_success(
        self,
        capability: str,
        model: str,
        stats: Dict[str, Any],
    ) -> None:
        """
        Add breadcrumb on successful call.

        Args:
            capability: Capability that was invoked
            model: Model that was used
            stats: Statistics about the call (latency, tokens, etc.)
        """
        add_success(
            layer=SDKLayer.ADAPTER.value,
            action=f"{self.name}_call_complete",
            message=f"{self.name} {capability} completed successfully",
            capability=capability,
            provider=self.name,
            model=model,
            stats=stats,
        )

    def _breadcrumb_call_error(
        self,
        capability: str,
        model: str,
        error: Exception,
        recommendations: Optional[List[str]] = None,
        retry_strategy: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Add breadcrumb on error.

        Args:
            capability: Capability that failed
            model: Model that was being used
            error: The exception that occurred
            recommendations: List of suggested actions to resolve the error
            retry_strategy: Retry configuration (max_retries, delay, etc.)
        """
        add_error(
            layer=SDKLayer.ADAPTER.value,
            action=f"{self.name}_call_failed",
            error=error,
            message=f"{self.name} {capability} failed: {error}",
            capability=capability,
            provider=self.name,
            model=model,
            recommendations=recommendations or [],
            retry_strategy=retry_strategy,
        )

    # --- Optional Capability Methods ---
    # Subclasses override the methods they support.
    # Default implementations raise NotImplementedError.

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
            model: TTS model to use
            voice: Voice ID or name
            **kwargs: Provider-specific parameters

        Returns:
            RawAudioResponse with audio data

        Raises:
            NotImplementedError: If adapter doesn't support TTS
        """
        raise NotImplementedError(
            f"{self.name} adapter does not support TTS capability"
        )

    async def tts_stream(
        self,
        text: str,
        model: str,
        voice: str,
        **kwargs: Any,
    ) -> Iterator[bytes]:
        """
        Stream text to speech audio chunks.

        Args:
            text: Text to convert
            model: TTS model to use
            voice: Voice ID or name
            **kwargs: Provider-specific parameters

        Yields:
            Audio data chunks

        Raises:
            NotImplementedError: If adapter doesn't support TTS streaming
        """
        raise NotImplementedError(
            f"{self.name} adapter does not support TTS streaming capability"
        )

    async def transcribe(
        self,
        audio: bytes,
        model: str,
        **kwargs: Any,
    ) -> str:
        """
        Transcribe audio to text (STT).

        Args:
            audio: Audio data bytes
            model: STT model to use
            **kwargs: Provider-specific parameters

        Returns:
            Transcribed text

        Raises:
            NotImplementedError: If adapter doesn't support STT
        """
        raise NotImplementedError(
            f"{self.name} adapter does not support STT capability"
        )

    async def embed(
        self,
        text: str,
        model: str,
        **kwargs: Any,
    ) -> List[float]:
        """
        Generate embedding vector for text.

        Args:
            text: Text to embed
            model: Embedding model to use
            **kwargs: Provider-specific parameters

        Returns:
            Embedding vector as list of floats

        Raises:
            NotImplementedError: If adapter doesn't support embeddings
        """
        raise NotImplementedError(
            f"{self.name} adapter does not support embedding capability"
        )

    async def embed_batch(
        self,
        texts: List[str],
        model: str,
        **kwargs: Any,
    ) -> List[List[float]]:
        """
        Generate embedding vectors for multiple texts.

        Args:
            texts: List of texts to embed
            model: Embedding model to use
            **kwargs: Provider-specific parameters

        Returns:
            List of embedding vectors

        Raises:
            NotImplementedError: If adapter doesn't support batch embeddings
        """
        raise NotImplementedError(
            f"{self.name} adapter does not support batch embedding capability"
        )

    async def complete(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        **kwargs: Any,
    ) -> str:
        """
        Generate text completion (LLM).

        Args:
            messages: Chat messages in OpenAI format
            model: LLM model to use
            **kwargs: Provider-specific parameters (temperature, max_tokens, etc.)

        Returns:
            Generated text response

        Raises:
            NotImplementedError: If adapter doesn't support text completion
        """
        raise NotImplementedError(
            f"{self.name} adapter does not support text completion capability"
        )
