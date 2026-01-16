"""
Base client infrastructure for Unified AI SDK.

Contains AdapterRegistry for managing provider adapters and
BaseCapabilityClient for implementing capability-specific clients.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, TypeVar

from ..adapters import BaseAdapter
from ..breadcrumbs import add_info, SDKLayer
from ..models import BaseRequest, BaseResponse, Capability


RequestT = TypeVar("RequestT", bound=BaseRequest)
ResponseT = TypeVar("ResponseT", bound=BaseResponse)


class AdapterRegistry:
    """
    Registry for provider adapters.

    Manages adapter instances by provider name and provides lookup
    by both name and model string (provider/model format).

    Example:
        registry = AdapterRegistry()
        registry.register(ElevenLabsAdapter(api_key="xi-..."))
        registry.register(GeminiAdapter(api_key="..."))

        adapter = registry.get("elevenlabs")
        adapter = registry.get_for_model("elevenlabs/eleven_multilingual_v2")
    """

    def __init__(self) -> None:
        """Initialize empty adapter registry."""
        self._adapters: Dict[str, BaseAdapter] = {}

    def register(self, adapter: BaseAdapter) -> None:
        """
        Register an adapter by its provider name.

        Args:
            adapter: Provider adapter instance to register

        Example:
            registry.register(ElevenLabsAdapter(api_key="xi-..."))
        """
        self._adapters[adapter.name] = adapter

    def get(self, name: str) -> Optional[BaseAdapter]:
        """
        Get adapter by provider name.

        Args:
            name: Provider name (e.g., "elevenlabs", "gemini")

        Returns:
            Adapter instance or None if not found
        """
        return self._adapters.get(name)

    def get_for_model(self, model_str: str) -> BaseAdapter:
        """
        Get adapter by parsing provider/model string.

        Args:
            model_str: Model string in "provider/model" format
                       e.g., "elevenlabs/eleven_multilingual_v2"

        Returns:
            Adapter instance for the provider

        Raises:
            ValueError: If model string is invalid or provider not registered
        """
        if "/" not in model_str:
            raise ValueError(
                f"Invalid model string '{model_str}': expected 'provider/model' format"
            )

        provider, _ = model_str.split("/", 1)
        adapter = self.get(provider)

        if adapter is None:
            available = ", ".join(self._adapters.keys()) or "none"
            raise ValueError(
                f"Provider '{provider}' not registered. Available: {available}"
            )

        return adapter

    def list_providers(self) -> List[str]:
        """
        List all registered provider names.

        Returns:
            List of provider names
        """
        return list(self._adapters.keys())

    def has_capability(self, provider: str, capability: Capability) -> bool:
        """
        Check if a provider supports a specific capability.

        Args:
            provider: Provider name
            capability: Capability to check

        Returns:
            True if provider supports capability, False otherwise
        """
        adapter = self.get(provider)
        if adapter is None:
            return False
        return adapter.supports(capability)

    def get_providers_for_capability(self, capability: Capability) -> List[str]:
        """
        Get all providers that support a specific capability.

        Args:
            capability: Capability to filter by

        Returns:
            List of provider names supporting the capability
        """
        return [
            name
            for name, adapter in self._adapters.items()
            if adapter.supports(capability)
        ]


class BaseCapabilityClient(ABC, Generic[RequestT, ResponseT]):
    """
    Base class for capability-specific clients (TTS, STT, Text, etc.).

    Provides common infrastructure for:
    - Registry-based adapter lookup
    - Fallback chain execution with breadcrumb tracking
    - Abstract capability identifier

    Subclasses implement specific capability logic (e.g., UnifiedTTSClient).

    Type Parameters:
        RequestT: Request type (e.g., TTSRequest)
        ResponseT: Response type (e.g., TTSResponse)

    Example:
        class UnifiedTTSClient(BaseCapabilityClient[TTSRequest, TTSResponse]):
            CAPABILITY = "tts"

            async def execute(self, request: TTSRequest, model: str) -> TTSResponse:
                # Implementation...
    """

    CAPABILITY: str = ""  # Must be set by subclasses: "tts", "text", etc.

    def __init__(
        self,
        registry: AdapterRegistry,
        fallback_chain: Optional[List[str]] = None,
    ) -> None:
        """
        Initialize capability client.

        Args:
            registry: AdapterRegistry with registered providers
            fallback_chain: List of model strings to try in order
                           e.g., ["elevenlabs/eleven_multilingual_v2", "gemini/gemini-2.0-flash"]
        """
        self.registry = registry
        self.fallback_chain: List[str] = fallback_chain or []

    @abstractmethod
    async def execute(self, request: RequestT, model: str) -> ResponseT:
        """
        Execute capability request on a specific model.

        Args:
            request: Capability-specific request
            model: Model string in "provider/model" format

        Returns:
            Capability-specific response

        Raises:
            ValueError: If model string is invalid
            ProviderError: If provider call fails
        """
        pass

    @abstractmethod
    async def execute_with_fallback(self, request: RequestT) -> ResponseT:
        """
        Execute with fallback chain, trying providers in order.

        Adds breadcrumbs at each step for debugging.

        Args:
            request: Capability-specific request

        Returns:
            Response from first successful provider

        Raises:
            AllProvidersFailedError: If all providers fail
        """
        pass

    def _parse_model_string(self, model_str: str) -> tuple[str, str]:
        """
        Parse provider/model string into components.

        Args:
            model_str: Model string in "provider/model" format

        Returns:
            Tuple of (provider, model_name)

        Raises:
            ValueError: If format is invalid
        """
        if "/" not in model_str:
            raise ValueError(
                f"Invalid model string '{model_str}': expected 'provider/model' format"
            )
        provider, model_name = model_str.split("/", 1)
        return provider, model_name

    def _breadcrumb_chain_start(self) -> None:
        """Add breadcrumb when starting fallback chain."""
        add_info(
            layer=SDKLayer.CLIENT.value,
            action="fallback_chain_start",
            message=f"Starting {self.CAPABILITY} with fallback chain: {self.fallback_chain}",
            capability=self.CAPABILITY,
            chain=self.fallback_chain,
        )

    def _breadcrumb_attempt(self, provider: str, model: str, attempt: int) -> None:
        """Add breadcrumb for each provider attempt."""
        add_info(
            layer=SDKLayer.CLIENT.value,
            action="provider_attempt",
            message=f"Attempting provider {attempt}/{len(self.fallback_chain)}: {provider}",
            provider=provider,
            model=model,
            attempt=attempt,
        )


__all__ = ["AdapterRegistry", "BaseCapabilityClient"]
