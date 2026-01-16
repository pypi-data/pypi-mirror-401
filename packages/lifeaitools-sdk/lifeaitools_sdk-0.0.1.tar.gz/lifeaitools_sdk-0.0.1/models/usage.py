"""Usage and cost tracking types for unified_ai SDK."""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class TokenUsage:
    """Token usage breakdown for LLM calls."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cache_creation_tokens: int = 0
    cache_read_tokens: int = 0

    @classmethod
    def from_openai(cls, usage: Dict[str, Any]) -> "TokenUsage":
        """Parse OpenAI usage response."""
        cached = usage.get("prompt_tokens_details", {}).get("cached_tokens", 0)
        return cls(
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            total_tokens=usage.get("total_tokens", 0),
            cache_read_tokens=cached,
        )

    @classmethod
    def from_anthropic(cls, usage: Dict[str, Any]) -> "TokenUsage":
        """Parse Anthropic usage response."""
        return cls(
            prompt_tokens=usage.get("input_tokens", 0),
            completion_tokens=usage.get("output_tokens", 0),
            total_tokens=usage.get("input_tokens", 0) + usage.get("output_tokens", 0),
            cache_creation_tokens=usage.get("cache_creation_input_tokens", 0),
            cache_read_tokens=usage.get("cache_read_input_tokens", 0),
        )


@dataclass
class AudioUsage:
    """Audio usage for TTS/STT calls."""
    duration_ms: int = 0
    characters_processed: int = 0
    segments_count: int = 0
    channels: int = 1


@dataclass
class CostBreakdown:
    """Cost breakdown in USD."""
    input_cost: float = 0.0
    output_cost: float = 0.0
    cache_write_cost: float = 0.0
    cache_read_cost: float = 0.0
    audio_cost: float = 0.0
    total_cost: float = 0.0
    currency: str = "USD"

    def to_dict(self) -> Dict[str, float]:
        return {
            "input_cost": self.input_cost,
            "output_cost": self.output_cost,
            "cache_write_cost": self.cache_write_cost,
            "cache_read_cost": self.cache_read_cost,
            "audio_cost": self.audio_cost,
            "total_cost": self.total_cost,
            "currency": self.currency,
        }


@dataclass
class UsageBreadcrumb:
    """Usage data for breadcrumb tracking."""
    provider: str
    model: str
    service: str  # "text", "tts", "stt"
    tokens: Optional[TokenUsage] = None
    audio: Optional[AudioUsage] = None
    cost: Optional[CostBreakdown] = None
    provider_usage: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_breadcrumb_dict(self) -> Dict[str, Any]:
        """Format for breadcrumb system."""
        result = {
            "event": "api_usage",
            "provider": self.provider,
            "model": self.model,
            "service": self.service,
            "timestamp": self.timestamp.isoformat() + "Z",
        }
        if self.tokens:
            result["tokens"] = {
                "prompt": self.tokens.prompt_tokens,
                "completion": self.tokens.completion_tokens,
                "total": self.tokens.total_tokens,
                "cache_creation": self.tokens.cache_creation_tokens,
                "cache_read": self.tokens.cache_read_tokens,
            }
        if self.audio:
            result["audio"] = {
                "duration_ms": self.audio.duration_ms,
                "characters": self.audio.characters_processed,
                "segments": self.audio.segments_count,
            }
        if self.cost:
            result["calculated_cost_usd"] = self.cost.total_cost
            result["cost_breakdown"] = self.cost.to_dict()
        if self.provider_usage:
            result["provider_usage"] = self.provider_usage
        return result
