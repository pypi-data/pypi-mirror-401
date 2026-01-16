"""Cost calculator using provider config pricing."""
from typing import Optional
from ..configs import get_provider_config
from ..models.usage import TokenUsage, AudioUsage, CostBreakdown


class CostCalculator:
    """Calculate API costs from usage data."""

    def __init__(self):
        self.config = get_provider_config()

    def calculate_llm_cost(
        self,
        provider: str,
        model: str,
        usage: TokenUsage,
    ) -> CostBreakdown:
        """Calculate LLM cost from token usage."""
        pricing = self.config.get_pricing(provider, "text", model)
        if not pricing:
            return CostBreakdown()

        # Calculate costs (prices are per 1M tokens)
        input_per_token = pricing.get("input_per_1m", 0) / 1_000_000
        output_per_token = pricing.get("output_per_1m", 0) / 1_000_000
        cache_write_per_token = pricing.get("cache_write_per_1m", 0) / 1_000_000
        cache_read_per_token = pricing.get("cache_read_per_1m", 0) / 1_000_000

        # Non-cached input tokens = total input - cached
        non_cached_input = usage.prompt_tokens - usage.cache_read_tokens

        input_cost = non_cached_input * input_per_token
        output_cost = usage.completion_tokens * output_per_token
        cache_write_cost = usage.cache_creation_tokens * cache_write_per_token
        cache_read_cost = usage.cache_read_tokens * cache_read_per_token

        return CostBreakdown(
            input_cost=input_cost,
            output_cost=output_cost,
            cache_write_cost=cache_write_cost,
            cache_read_cost=cache_read_cost,
            total_cost=input_cost + output_cost + cache_write_cost + cache_read_cost,
        )

    def calculate_tts_cost(
        self,
        provider: str,
        model: str,
        characters: int,
    ) -> CostBreakdown:
        """Calculate TTS cost from character count."""
        pricing = self.config.get_pricing(provider, "tts", model)
        if not pricing:
            return CostBreakdown()

        per_1k_chars = pricing.get("per_1k_chars", 0)
        audio_cost = (characters / 1000) * per_1k_chars

        return CostBreakdown(audio_cost=audio_cost, total_cost=audio_cost)

    def calculate_stt_cost(
        self,
        provider: str,
        model: str,
        duration_ms: int,
    ) -> CostBreakdown:
        """Calculate STT cost from audio duration."""
        pricing = self.config.get_pricing(provider, "stt", model)
        if not pricing:
            return CostBreakdown()

        duration_minutes = duration_ms / 60_000

        if "per_minute" in pricing:
            audio_cost = duration_minutes * pricing["per_minute"]
        elif "per_hour" in pricing:
            audio_cost = (duration_minutes / 60) * pricing["per_hour"]
        else:
            audio_cost = 0.0

        return CostBreakdown(audio_cost=audio_cost, total_cost=audio_cost)


# Singleton instance
_calculator: Optional[CostCalculator] = None


def get_cost_calculator() -> CostCalculator:
    global _calculator
    if _calculator is None:
        _calculator = CostCalculator()
    return _calculator
