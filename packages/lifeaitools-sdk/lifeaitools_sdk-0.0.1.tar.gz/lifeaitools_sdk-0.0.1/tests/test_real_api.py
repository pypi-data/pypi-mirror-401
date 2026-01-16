#!/usr/bin/env python3
"""
Real API Tests for Unified AI SDK.

Script: test_real_api.py
Created: 2026-01-13
Purpose: Test SDK with real APIs using minimal token consumption
Keywords: real-api, integration, gemini, elevenlabs, json-schema
Status: active
Prerequisites:
  - Set GOOGLE_API_KEY in environment
  - Set ELEVENLABS_API_KEY in environment (optional for TTS tests)
See-Also: ../adapters/gemini.py, ../adapters/elevenlabs.py

SAFETY FEATURES:
- MAX_RETRIES: Prevents infinite retry loops
- TIMEOUT_SECONDS: Hard timeout for all API calls
- MAX_TOKENS: Caps token usage per request
- SMALL_PROMPTS: Uses minimal prompts to reduce cost

Usage:
    # From unified_ai directory:
    cd /mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai

    # Load env and run:
    set -a && source ../../services/llm_orchestrator/.env && set +a
    PYTHONPATH=.. python tests/test_real_api.py

    # Or run specific tests:
    PYTHONPATH=.. python tests/test_real_api.py --test gemini_text
    PYTHONPATH=.. python tests/test_real_api.py --test json_schema
    PYTHONPATH=.. python tests/test_real_api.py --test tts
"""

import asyncio
import json
import os
import signal
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

# Safety limits - CRITICAL: prevents token burning
MAX_RETRIES = 2  # Max retries per test
TIMEOUT_SECONDS = 30  # Hard timeout per test
MAX_TOKENS_TEXT = 50  # Small token limit for text tests
MAX_CHARS_TTS = 20  # Max chars for TTS tests

# Small prompts to minimize cost
SMALL_PROMPT = "Say hi"
JSON_PROMPT = "Return {\"greeting\": \"hello\"}"


@dataclass
class TestResult:
    """Result of a single test."""
    name: str
    success: bool
    duration_ms: float
    message: str
    cost_estimate: Optional[float] = None
    details: Optional[Dict[str, Any]] = None


class TimeoutError(Exception):
    """Raised when a test times out."""
    pass


def timeout_handler(signum, frame):
    """Signal handler for timeout."""
    raise TimeoutError(f"Test timed out after {TIMEOUT_SECONDS}s")


async def run_with_timeout(coro, timeout: int = TIMEOUT_SECONDS):
    """Run coroutine with timeout protection."""
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        raise TimeoutError(f"Test timed out after {timeout}s")


class RealAPITester:
    """
    Real API tester with safety protections.

    Features:
    - Timeout protection on all calls
    - Retry limits to prevent infinite loops
    - Small prompts to minimize token usage
    - JSON schema enforcement testing
    """

    def __init__(self):
        self.results: List[TestResult] = []
        # Support both GOOGLE_API_KEY and GEMINI_API_KEY
        self.google_api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
        self.openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")

        print("=== Unified AI SDK - Real API Tests ===")
        print(f"Safety limits: MAX_RETRIES={MAX_RETRIES}, TIMEOUT={TIMEOUT_SECONDS}s")
        print(f"Token limits: MAX_TOKENS={MAX_TOKENS_TEXT}, MAX_CHARS_TTS={MAX_CHARS_TTS}")
        print()
        print("Available API keys:")
        print(f"  GEMINI_API_KEY:     {'set' if self.google_api_key else 'NOT SET'}")
        print(f"  ELEVENLABS_API_KEY: {'set' if self.elevenlabs_api_key else 'NOT SET'}")
        print(f"  OPENAI_API_KEY:     {'set' if self.openai_api_key else 'NOT SET'}")
        print(f"  ANTHROPIC_API_KEY:  {'set' if self.anthropic_api_key else 'NOT SET'}")
        print(f"  OPENROUTER_API_KEY: {'set' if self.openrouter_api_key else 'NOT SET'}")
        print()

    def _record_result(self, name: str, success: bool, duration_ms: float,
                       message: str, cost: float = None, details: Dict = None):
        """Record test result."""
        result = TestResult(
            name=name,
            success=success,
            duration_ms=duration_ms,
            message=message,
            cost_estimate=cost,
            details=details,
        )
        self.results.append(result)

        status = "PASS" if success else "FAIL"
        cost_str = f" (${cost:.6f})" if cost else ""
        print(f"[{status}] {name}: {message}{cost_str} [{duration_ms:.0f}ms]")

    async def test_gemini_text_basic(self) -> bool:
        """Test basic Gemini text generation."""
        if not self.google_api_key:
            self._record_result(
                "gemini_text_basic", False, 0,
                "SKIPPED - GOOGLE_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.gemini import GeminiAdapter

            adapter = GeminiAdapter(api_key=self.google_api_key)

            # Minimal prompt test
            result = await run_with_timeout(
                adapter.complete(
                    messages=[{"role": "user", "content": SMALL_PROMPT}],
                    model="gemini-2.0-flash",
                    max_tokens=MAX_TOKENS_TEXT,
                    temperature=0,  # Deterministic for testing
                ),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000
            content = result.get("content", "")
            usage = result.get("usage", {})

            if content and len(content) > 0:
                self._record_result(
                    "gemini_text_basic", True, duration_ms,
                    f"Got response: '{content[:50]}...'",
                    details={"usage": usage, "content_length": len(content)},
                )
                return True
            else:
                self._record_result(
                    "gemini_text_basic", False, duration_ms,
                    "Empty response"
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "gemini_text_basic", False, duration_ms,
                f"Error: {str(e)[:100]}"
            )
            return False

    async def test_gemini_json_schema(self) -> bool:
        """Test Gemini JSON schema enforcement (strict mode)."""
        if not self.google_api_key:
            self._record_result(
                "gemini_json_schema", False, 0,
                "SKIPPED - GOOGLE_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.gemini import GeminiAdapter

            adapter = GeminiAdapter(api_key=self.google_api_key)

            # Define strict JSON schema
            schema = {
                "type": "object",
                "properties": {
                    "greeting": {"type": "string"},
                    "language": {"type": "string"}
                },
                "required": ["greeting", "language"]
            }

            result = await run_with_timeout(
                adapter.complete(
                    messages=[{"role": "user", "content": "Say hello in English"}],
                    model="gemini-2.0-flash",
                    max_tokens=MAX_TOKENS_TEXT,
                    temperature=0,
                    response_format={
                        "type": "json_schema",
                        "json_schema": schema
                    }
                ),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000
            content = result.get("content", "")

            # Validate JSON structure
            try:
                parsed = json.loads(content)
                has_greeting = "greeting" in parsed
                has_language = "language" in parsed

                if has_greeting and has_language:
                    self._record_result(
                        "gemini_json_schema", True, duration_ms,
                        f"Valid JSON schema: {parsed}",
                        details={"parsed": parsed},
                    )
                    return True
                else:
                    self._record_result(
                        "gemini_json_schema", False, duration_ms,
                        f"Missing fields. Got: {parsed}"
                    )
                    return False

            except json.JSONDecodeError as e:
                self._record_result(
                    "gemini_json_schema", False, duration_ms,
                    f"Invalid JSON: {content[:50]}... Error: {e}"
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "gemini_json_schema", False, duration_ms,
                f"Error: {str(e)[:100]}"
            )
            return False

    async def test_gemini_json_object(self) -> bool:
        """Test Gemini basic JSON object mode."""
        if not self.google_api_key:
            self._record_result(
                "gemini_json_object", False, 0,
                "SKIPPED - GOOGLE_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.gemini import GeminiAdapter

            adapter = GeminiAdapter(api_key=self.google_api_key)

            result = await run_with_timeout(
                adapter.complete(
                    messages=[{"role": "user", "content": JSON_PROMPT}],
                    model="gemini-2.0-flash",
                    max_tokens=MAX_TOKENS_TEXT,
                    temperature=0,
                    response_format={"type": "json_object"}
                ),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000
            content = result.get("content", "")

            try:
                parsed = json.loads(content)
                self._record_result(
                    "gemini_json_object", True, duration_ms,
                    f"Valid JSON: {parsed}",
                    details={"parsed": parsed},
                )
                return True
            except json.JSONDecodeError:
                self._record_result(
                    "gemini_json_object", False, duration_ms,
                    f"Invalid JSON: {content[:50]}..."
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "gemini_json_object", False, duration_ms,
                f"Error: {str(e)[:100]}"
            )
            return False

    async def test_elevenlabs_tts(self) -> bool:
        """Test ElevenLabs TTS with minimal text."""
        if not self.elevenlabs_api_key:
            self._record_result(
                "elevenlabs_tts", False, 0,
                "SKIPPED - ELEVENLABS_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.elevenlabs import ElevenLabsAdapter

            adapter = ElevenLabsAdapter(api_key=self.elevenlabs_api_key)

            # Minimal text for TTS
            test_text = "Hi"  # Just 2 chars

            # Use voice_id (21m00Tcm4TlvDq8ikWAM is Rachel's ID)
            result = await run_with_timeout(
                adapter.tts(
                    text=test_text,
                    model="eleven_multilingual_v2",
                    voice="21m00Tcm4TlvDq8ikWAM",  # Rachel's voice ID
                ),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000

            if result.data and len(result.data) > 0:
                self._record_result(
                    "elevenlabs_tts", True, duration_ms,
                    f"Got audio: {len(result.data)} bytes, format={result.format.value}",
                    details={
                        "audio_bytes": len(result.data),
                        "format": result.format.value,
                        "sample_rate": result.sample_rate,
                    },
                )
                return True
            else:
                self._record_result(
                    "elevenlabs_tts", False, duration_ms,
                    "Empty audio response"
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "elevenlabs_tts", False, duration_ms,
                f"Error: {str(e)[:100]}"
            )
            return False

    async def test_gemini_tts(self) -> bool:
        """Test Gemini TTS with minimal text."""
        if not self.google_api_key:
            self._record_result(
                "gemini_tts", False, 0,
                "SKIPPED - GOOGLE_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.gemini import GeminiAdapter

            adapter = GeminiAdapter(api_key=self.google_api_key)

            # Gemini TTS needs slightly longer text
            test_text = "Hello, how are you today?"

            result = await run_with_timeout(
                adapter.tts(
                    text=test_text,
                    model="gemini-2.5-flash-preview-tts",
                    voice="Puck",
                    output_format="mp3",
                ),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000

            if result.data and len(result.data) > 0:
                self._record_result(
                    "gemini_tts", True, duration_ms,
                    f"Got audio: {len(result.data)} bytes, format={result.format.value}",
                    details={
                        "audio_bytes": len(result.data),
                        "format": result.format.value,
                    },
                )
                return True
            else:
                self._record_result(
                    "gemini_tts", False, duration_ms,
                    "Empty audio response"
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "gemini_tts", False, duration_ms,
                f"Error: {str(e)[:100]}"
            )
            return False

    async def test_openai_text(self) -> bool:
        """Test OpenAI text generation."""
        if not self.openai_api_key:
            self._record_result(
                "openai_text", False, 0,
                "SKIPPED - OPENAI_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.openai import OpenAIAdapter

            adapter = OpenAIAdapter(api_key=self.openai_api_key)

            result = await run_with_timeout(
                adapter.complete(
                    messages=[{"role": "user", "content": SMALL_PROMPT}],
                    model="gpt-4o-mini",
                    max_tokens=MAX_TOKENS_TEXT,
                    temperature=0,
                ),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000
            content = result.get("content", "")

            if content:
                self._record_result(
                    "openai_text", True, duration_ms,
                    f"Response: '{content[:50]}...'",
                    details={"usage": result.get("usage", {})},
                )
                return True
            else:
                self._record_result(
                    "openai_text", False, duration_ms,
                    "Empty response"
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "openai_text", False, duration_ms,
                f"Error: {str(e)[:100]}"
            )
            return False

    async def test_openai_tts(self) -> bool:
        """Test OpenAI TTS."""
        if not self.openai_api_key:
            self._record_result(
                "openai_tts", False, 0,
                "SKIPPED - OPENAI_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.openai import OpenAIAdapter

            adapter = OpenAIAdapter(api_key=self.openai_api_key)

            result = await run_with_timeout(
                adapter.tts(
                    text="Hi",
                    model="tts-1",
                    voice="alloy",
                ),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000

            if result.data and len(result.data) > 0:
                self._record_result(
                    "openai_tts", True, duration_ms,
                    f"Got audio: {len(result.data)} bytes, format={result.format.value}",
                )
                return True
            else:
                self._record_result(
                    "openai_tts", False, duration_ms,
                    "Empty audio response"
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "openai_tts", False, duration_ms,
                f"Error: {str(e)[:100]}"
            )
            return False

    async def test_anthropic_text(self) -> bool:
        """Test Anthropic Claude text generation."""
        if not self.anthropic_api_key:
            self._record_result(
                "anthropic_text", False, 0,
                "SKIPPED - ANTHROPIC_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.anthropic import AnthropicAdapter

            adapter = AnthropicAdapter(api_key=self.anthropic_api_key)

            result = await run_with_timeout(
                adapter.complete(
                    messages=[{"role": "user", "content": SMALL_PROMPT}],
                    model="claude-3-5-haiku-20241022",
                    max_tokens=MAX_TOKENS_TEXT,  # Required for Anthropic
                    temperature=0,
                ),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000
            content = result.get("content", "")

            if content:
                self._record_result(
                    "anthropic_text", True, duration_ms,
                    f"Response: '{content[:50]}...'",
                    details={"usage": result.get("usage", {})},
                )
                return True
            else:
                self._record_result(
                    "anthropic_text", False, duration_ms,
                    "Empty response"
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "anthropic_text", False, duration_ms,
                f"Error: {str(e)[:200]}"  # Show more error details
            )
            return False

    async def test_openrouter_text(self) -> bool:
        """Test OpenRouter text generation."""
        if not self.openrouter_api_key:
            self._record_result(
                "openrouter_text", False, 0,
                "SKIPPED - OPENROUTER_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.openrouter import OpenRouterAdapter

            adapter = OpenRouterAdapter(api_key=self.openrouter_api_key)

            # Use a cheap model for testing
            result = await run_with_timeout(
                adapter.complete(
                    messages=[{"role": "user", "content": SMALL_PROMPT}],
                    model="google/gemini-2.0-flash-001",  # Cheap model
                    max_tokens=MAX_TOKENS_TEXT,
                    temperature=0,
                ),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000
            content = result.get("content", "")

            if content:
                self._record_result(
                    "openrouter_text", True, duration_ms,
                    f"Response: '{content[:50]}...'",
                    details={"usage": result.get("usage", {})},
                )
                return True
            else:
                self._record_result(
                    "openrouter_text", False, duration_ms,
                    "Empty response"
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "openrouter_text", False, duration_ms,
                f"Error: {str(e)[:100]}"
            )
            return False

    async def test_unified_text_client(self) -> bool:
        """Test UnifiedTextClient with Gemini backend."""
        if not self.google_api_key:
            self._record_result(
                "unified_text_client", False, 0,
                "SKIPPED - GOOGLE_API_KEY not set"
            )
            return False

        start = time.time()
        try:
            from unified_ai.adapters.gemini import GeminiAdapter
            from unified_ai.clients.base import AdapterRegistry
            from unified_ai.clients.text import UnifiedTextClient
            from unified_ai.models import TextRequest

            # Setup registry
            registry = AdapterRegistry()
            gemini = GeminiAdapter(api_key=self.google_api_key)
            registry.register(gemini)  # register() takes adapter only

            # Create client
            client = UnifiedTextClient(registry=registry, fallback_chain=[])

            # Create request
            request = TextRequest(
                prompt=SMALL_PROMPT,
                max_tokens=MAX_TOKENS_TEXT,
                temperature=0,
            )

            # Execute
            response = await run_with_timeout(
                client.execute(request, "gemini/gemini-2.0-flash"),
                timeout=TIMEOUT_SECONDS,
            )

            duration_ms = (time.time() - start) * 1000

            if response.success and response.content:
                self._record_result(
                    "unified_text_client", True, duration_ms,
                    f"Response: '{response.content[:50]}...'",
                    details={
                        "provider": response.provider,
                        "model": response.model,
                        "usage": response.usage,
                    },
                )
                return True
            else:
                self._record_result(
                    "unified_text_client", False, duration_ms,
                    f"Failed: success={response.success}"
                )
                return False

        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self._record_result(
                "unified_text_client", False, duration_ms,
                f"Error: {str(e)[:100]}"
            )
            return False

    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests with safety protections."""
        print("\n" + "=" * 60)
        print("Running tests...")
        print("=" * 60 + "\n")

        # Run tests sequentially to avoid rate limits
        # Text generation tests (all providers)
        await self.test_openai_text()
        await self.test_anthropic_text()
        await self.test_openrouter_text()
        await self.test_gemini_text_basic()

        # JSON mode tests
        await self.test_gemini_json_object()
        await self.test_gemini_json_schema()

        # TTS tests
        await self.test_openai_tts()
        await self.test_elevenlabs_tts()
        await self.test_gemini_tts()

        # Client tests
        await self.test_unified_text_client()

        # Summary
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        passed = sum(1 for r in self.results if r.success)
        failed = sum(1 for r in self.results if not r.success and "SKIPPED" not in r.message)
        skipped = sum(1 for r in self.results if "SKIPPED" in r.message)

        print(f"PASSED: {passed}")
        print(f"FAILED: {failed}")
        print(f"SKIPPED: {skipped}")
        print(f"TOTAL: {len(self.results)}")

        return {
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "total": len(self.results),
            "results": [
                {
                    "name": r.name,
                    "success": r.success,
                    "message": r.message,
                    "duration_ms": r.duration_ms,
                }
                for r in self.results
            ],
        }

    async def run_single_test(self, test_name: str) -> bool:
        """Run a single test by name."""
        test_map = {
            # Text tests
            "openai_text": self.test_openai_text,
            "anthropic_text": self.test_anthropic_text,
            "openrouter_text": self.test_openrouter_text,
            "gemini_text": self.test_gemini_text_basic,
            # JSON tests
            "json_object": self.test_gemini_json_object,
            "json_schema": self.test_gemini_json_schema,
            # TTS tests
            "openai_tts": self.test_openai_tts,
            "elevenlabs_tts": self.test_elevenlabs_tts,
            "gemini_tts": self.test_gemini_tts,
            "tts": self.test_elevenlabs_tts,  # Alias
            # Client tests
            "unified_client": self.test_unified_text_client,
        }

        if test_name not in test_map:
            print(f"Unknown test: {test_name}")
            print(f"Available tests: {', '.join(test_map.keys())}")
            return False

        return await test_map[test_name]()


async def main():
    """Main entry point."""
    tester = RealAPITester()

    # Check for specific test argument
    if len(sys.argv) > 2 and sys.argv[1] == "--test":
        test_name = sys.argv[2]
        await tester.run_single_test(test_name)
    else:
        results = await tester.run_all_tests()

        # Exit with error code if tests failed
        if results["failed"] > 0:
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
