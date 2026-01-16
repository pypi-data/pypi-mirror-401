"""
Exceptions for Unified AI SDK

All exceptions include fields for breadcrumb integration:
- recommendations: List of actionable suggestions
- retry_strategy: Dict with is_retryable, retry_after, alternatives
- breadcrumbs: Full breadcrumb trail up to this error
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class SDKError(Exception):
    """Base exception with breadcrumb fields"""
    message: str
    recommendations: List[str] = field(default_factory=list)
    retry_strategy: Optional[Dict[str, Any]] = None
    breadcrumbs: List[Dict[str, Any]] = field(default_factory=list)

    def __str__(self):
        return self.message


@dataclass
class ProviderError(SDKError):
    """Error from a specific provider"""
    provider: str = ""
    model: str = ""
    http_status: Optional[int] = None
    provider_error_code: Optional[str] = None


@dataclass
class RateLimitError(ProviderError):
    """Rate limit exceeded"""
    retry_after_seconds: int = 60

    def __post_init__(self):
        self.retry_strategy = {
            "is_retryable": True,
            "retry_after_seconds": self.retry_after_seconds,
            "max_retries": 3
        }
        if not self.recommendations:
            self.recommendations = [
                f"Wait {self.retry_after_seconds} seconds before retrying",
                "Implement exponential backoff",
                "Consider switching to alternative provider"
            ]


@dataclass
class QuotaExceededError(ProviderError):
    """Quota/credits exhausted - NOT retryable"""

    def __post_init__(self):
        self.retry_strategy = {
            "is_retryable": False,
            "reason": "Quota exhausted - requires account upgrade"
        }
        if not self.recommendations:
            self.recommendations = [
                "Check account balance/quota",
                "Switch to different provider",
                "Upgrade plan for more quota"
            ]


@dataclass
class AllProvidersFailedError(SDKError):
    """All providers in fallback chain failed"""
    failed_providers: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        provider_summary = ", ".join(
            f"{p['provider']} ({p.get('error', 'unknown')})"
            for p in self.failed_providers
        )
        self.message = f"All providers failed: {provider_summary}"
        self.retry_strategy = {"is_retryable": False}
        if not self.recommendations:
            self.recommendations = [
                "Check all provider API keys",
                "Verify network connectivity",
                "Check provider status pages"
            ]


@dataclass
class ValidationError(SDKError):
    """Request validation failed"""
    pass


@dataclass
class ConfigurationError(SDKError):
    """Configuration or setup error"""
    pass
