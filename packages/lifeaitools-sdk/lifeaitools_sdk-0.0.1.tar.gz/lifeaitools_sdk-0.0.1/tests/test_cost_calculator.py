"""
Tests for cost calculation utilities.

Tests cover:
- LLM cost calculation with cache tokens
- TTS cost per 1k characters
- STT cost per minute/hour
- Zero cost for missing pricing
"""
import pytest
from unified_ai.utils.cost_calculator import get_cost_calculator, CostCalculator
from unified_ai.models.usage import TokenUsage, CostBreakdown


class TestCostCalculatorSingleton:
    """Test cost calculator singleton behavior."""

    def test_get_cost_calculator_returns_instance(self):
        """get_cost_calculator should return a CostCalculator instance."""
        calc = get_cost_calculator()
        assert isinstance(calc, CostCalculator)

    def test_get_cost_calculator_returns_same_instance(self):
        """get_cost_calculator should return the same singleton instance."""
        calc1 = get_cost_calculator()
        calc2 = get_cost_calculator()
        assert calc1 is calc2


class TestLLMCostCalculation:
    """Test LLM cost calculations."""

    def test_basic_llm_cost(self):
        """Calculate cost for simple token usage."""
        calc = get_cost_calculator()
        usage = TokenUsage(
            prompt_tokens=1000,
            completion_tokens=500,
            total_tokens=1500,
        )
        cost = calc.calculate_llm_cost("openai", "gpt-4o", usage)

        assert isinstance(cost, CostBreakdown)
        assert cost.total_cost > 0
        # gpt-4o: input $2.50/1M, output $10.00/1M
        # Expected: 1000 * 2.50/1M + 500 * 10.00/1M = 0.0025 + 0.005 = 0.0075
        assert abs(cost.total_cost - 0.0075) < 0.0001

    def test_llm_cost_with_cache_tokens(self):
        """Calculate cost with prompt caching (Anthropic-style)."""
        calc = get_cost_calculator()
        usage = TokenUsage(
            prompt_tokens=2000,
            completion_tokens=500,
            total_tokens=2500,
            cache_creation_tokens=500,
            cache_read_tokens=500,
        )
        cost = calc.calculate_llm_cost("anthropic", "claude-sonnet-4-20250514", usage)

        assert isinstance(cost, CostBreakdown)
        assert cost.cache_write_cost > 0
        assert cost.cache_read_cost > 0
        # Non-cached input = 2000 - 500 = 1500 tokens
        # claude-sonnet-4: input $3.00/1M, output $15.00/1M
        # cache_write $3.75/1M, cache_read $0.30/1M
        assert cost.input_cost > 0
        assert cost.output_cost > 0
        assert cost.total_cost == (
            cost.input_cost + cost.output_cost +
            cost.cache_write_cost + cost.cache_read_cost
        )

    def test_llm_cost_with_openai_cached_tokens(self):
        """Calculate cost with OpenAI-style cached tokens."""
        calc = get_cost_calculator()
        usage = TokenUsage(
            prompt_tokens=1000,
            completion_tokens=500,
            total_tokens=1500,
            cache_read_tokens=200,  # OpenAI reports cached tokens in prompt
        )
        cost = calc.calculate_llm_cost("openai", "gpt-4o", usage)

        assert isinstance(cost, CostBreakdown)
        # Non-cached input = 1000 - 200 = 800 tokens
        # gpt-4o: input $2.50/1M, output $10.00/1M, cache_read $0.625/1M
        assert cost.cache_read_cost > 0

    def test_zero_cost_for_missing_pricing(self):
        """Return zero cost when pricing is not found."""
        calc = get_cost_calculator()
        usage = TokenUsage(
            prompt_tokens=1000,
            completion_tokens=500,
            total_tokens=1500,
        )
        # Use a non-existent model
        cost = calc.calculate_llm_cost("openai", "nonexistent-model", usage)

        assert isinstance(cost, CostBreakdown)
        assert cost.total_cost == 0
        assert cost.input_cost == 0
        assert cost.output_cost == 0


class TestTTSCostCalculation:
    """Test TTS cost calculations."""

    def test_tts_cost_per_1k_characters(self):
        """Calculate TTS cost based on character count."""
        calc = get_cost_calculator()
        # 1000 characters with tts-1 at $0.015/1k chars
        cost = calc.calculate_tts_cost("openai", "tts-1", 1000)

        assert isinstance(cost, CostBreakdown)
        assert cost.audio_cost > 0
        assert cost.total_cost == cost.audio_cost
        # Expected: 1000 chars * $0.015/1k = $0.015
        assert abs(cost.total_cost - 0.015) < 0.0001

    def test_tts_cost_hd_model(self):
        """TTS-1-HD should cost more than TTS-1."""
        calc = get_cost_calculator()
        cost_standard = calc.calculate_tts_cost("openai", "tts-1", 1000)
        cost_hd = calc.calculate_tts_cost("openai", "tts-1-hd", 1000)

        assert cost_hd.total_cost > cost_standard.total_cost
        # tts-1: $0.015/1k, tts-1-hd: $0.030/1k
        assert abs(cost_hd.total_cost / cost_standard.total_cost - 2.0) < 0.01

    def test_tts_cost_scales_with_characters(self):
        """TTS cost should scale linearly with character count."""
        calc = get_cost_calculator()
        cost_1k = calc.calculate_tts_cost("openai", "tts-1", 1000)
        cost_2k = calc.calculate_tts_cost("openai", "tts-1", 2000)

        assert abs(cost_2k.total_cost / cost_1k.total_cost - 2.0) < 0.01

    def test_tts_zero_cost_for_missing_pricing(self):
        """Return zero cost for unknown TTS model."""
        calc = get_cost_calculator()
        cost = calc.calculate_tts_cost("openai", "nonexistent-tts-model", 1000)

        assert isinstance(cost, CostBreakdown)
        assert cost.total_cost == 0
        assert cost.audio_cost == 0


class TestSTTCostCalculation:
    """Test STT cost calculations."""

    def test_stt_cost_per_minute(self):
        """Calculate STT cost based on audio duration in minutes."""
        calc = get_cost_calculator()
        # 60000 ms = 1 minute, whisper-1 at $0.006/minute
        cost = calc.calculate_stt_cost("openai", "whisper-1", 60000)

        assert isinstance(cost, CostBreakdown)
        assert cost.audio_cost > 0
        assert cost.total_cost == cost.audio_cost
        # Expected: 1 minute * $0.006 = $0.006
        assert abs(cost.total_cost - 0.006) < 0.0001

    def test_stt_cost_fractional_minutes(self):
        """STT cost should work with fractional minutes."""
        calc = get_cost_calculator()
        # 30000 ms = 0.5 minutes
        cost = calc.calculate_stt_cost("openai", "whisper-1", 30000)

        # Expected: 0.5 minutes * $0.006 = $0.003
        assert abs(cost.total_cost - 0.003) < 0.0001

    def test_stt_cost_scales_with_duration(self):
        """STT cost should scale linearly with duration."""
        calc = get_cost_calculator()
        cost_1min = calc.calculate_stt_cost("openai", "whisper-1", 60000)
        cost_5min = calc.calculate_stt_cost("openai", "whisper-1", 300000)

        assert abs(cost_5min.total_cost / cost_1min.total_cost - 5.0) < 0.01

    def test_stt_zero_cost_for_missing_pricing(self):
        """Return zero cost for unknown STT model."""
        calc = get_cost_calculator()
        cost = calc.calculate_stt_cost("openai", "nonexistent-stt-model", 60000)

        assert isinstance(cost, CostBreakdown)
        assert cost.total_cost == 0
        assert cost.audio_cost == 0

    def test_stt_cost_zero_duration(self):
        """Zero duration should result in zero cost."""
        calc = get_cost_calculator()
        cost = calc.calculate_stt_cost("openai", "whisper-1", 0)

        assert cost.total_cost == 0
        assert cost.audio_cost == 0


class TestCostBreakdownIntegrity:
    """Test CostBreakdown dataclass integrity."""

    def test_cost_breakdown_defaults(self):
        """CostBreakdown should have sensible defaults."""
        breakdown = CostBreakdown()
        assert breakdown.input_cost == 0.0
        assert breakdown.output_cost == 0.0
        assert breakdown.cache_write_cost == 0.0
        assert breakdown.cache_read_cost == 0.0
        assert breakdown.audio_cost == 0.0
        assert breakdown.total_cost == 0.0
        assert breakdown.currency == "USD"

    def test_cost_breakdown_to_dict(self):
        """CostBreakdown.to_dict should return all fields."""
        breakdown = CostBreakdown(
            input_cost=0.01,
            output_cost=0.02,
            total_cost=0.03,
        )
        result = breakdown.to_dict()

        assert isinstance(result, dict)
        assert "input_cost" in result
        assert "output_cost" in result
        assert "total_cost" in result
        assert "currency" in result
        assert result["total_cost"] == 0.03


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
