"""
Breadcrumb System for Unified AI SDK

Tracks processing through all layers for debugging and observability.
Ported from: llm-handler-api/app/core/breadcrumb_types.py
"""
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
import threading


class BreadcrumbLevel(str, Enum):
    SUCCESS = "SUCCESS"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"


class SDKLayer(str, Enum):
    SDK = "SDK"                   # UnifiedAI entry point
    CLIENT = "Client"             # Capability clients (TTS, LLM)
    ADAPTER = "Adapter"           # Provider adapters
    PREPROCESSOR = "Preprocessor" # Pre-processing hooks
    POSTPROCESSOR = "Postprocessor"
    RETRY = "Retry"               # Retry logic
    FALLBACK = "Fallback"         # Fallback handling


@dataclass
class BreadcrumbCollector:
    """Collects breadcrumbs for a single request execution"""
    request_id: str
    breadcrumbs: List[Dict[str, Any]] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def add(
        self,
        layer: str,
        action: str,
        level: BreadcrumbLevel = BreadcrumbLevel.INFO,
        message: Optional[str] = None,
        **kwargs
    ) -> None:
        """Add breadcrumb to collection"""
        breadcrumb = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "layer": layer,
            "action": action,
            "level": level.value,
        }
        if message:
            breadcrumb["message"] = message
        breadcrumb.update(kwargs)

        with self._lock:
            self.breadcrumbs.append(breadcrumb)

    def get_all(self) -> List[Dict[str, Any]]:
        """Get all breadcrumbs"""
        return self.breadcrumbs.copy()

    def get_errors(self) -> List[Dict[str, Any]]:
        """Get only error breadcrumbs"""
        return [b for b in self.breadcrumbs if b.get("level") == "ERROR"]

    def get_warnings(self) -> List[Dict[str, Any]]:
        """Get warnings for quick visibility"""
        return [b for b in self.breadcrumbs if b.get("level") == "WARN"]


# Context variable for current request's breadcrumbs
_current_collector: ContextVar[Optional[BreadcrumbCollector]] = ContextVar(
    'breadcrumb_collector', default=None
)


def start_collection(request_id: str) -> BreadcrumbCollector:
    """Start collecting breadcrumbs for a request"""
    collector = BreadcrumbCollector(request_id=request_id)
    _current_collector.set(collector)
    return collector


def get_collector() -> Optional[BreadcrumbCollector]:
    """Get current request's breadcrumb collector"""
    return _current_collector.get()


def add_breadcrumb(
    layer: str,
    action: str,
    level: BreadcrumbLevel = BreadcrumbLevel.INFO,
    message: Optional[str] = None,
    **kwargs
) -> None:
    """Add breadcrumb to current collection (if active)"""
    collector = get_collector()
    if collector:
        collector.add(layer, action, level, message, **kwargs)


# Convenience helpers
def add_success(layer: str, action: str, message: str, **kwargs) -> None:
    add_breadcrumb(layer, action, BreadcrumbLevel.SUCCESS, message, **kwargs)


def add_info(layer: str, action: str, message: str, **kwargs) -> None:
    add_breadcrumb(layer, action, BreadcrumbLevel.INFO, message, **kwargs)


def add_warning(layer: str, action: str, message: str, **kwargs) -> None:
    add_breadcrumb(layer, action, BreadcrumbLevel.WARN, message, **kwargs)


def add_error(
    layer: str,
    action: str,
    error: Exception,
    message: Optional[str] = None,
    recommendations: Optional[List[str]] = None,
    retry_strategy: Optional[Dict] = None,
    **kwargs
) -> None:
    if not message:
        message = f"{type(error).__name__}: {str(error)}"

    add_breadcrumb(
        layer, action, BreadcrumbLevel.ERROR, message,
        error={"type": type(error).__name__, "message": str(error)},
        recommendations=recommendations,
        retry_strategy=retry_strategy,
        **kwargs
    )
