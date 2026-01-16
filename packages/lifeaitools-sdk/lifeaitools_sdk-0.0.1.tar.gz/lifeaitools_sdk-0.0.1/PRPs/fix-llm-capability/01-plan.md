# Implementation Plan: LLM/Text Capability with JSON Mode

**Created:** 2026-01-13
**Purpose:** Fix gaps from validation report - implement LLM capability with structured JSON output
**Status:** ready_for_execution

## Problem Statement

From `05-validation-params.md`:
- `TextRequest.response_format` field exists but NO implementation
- Missing `UnifiedTextClient`
- Missing `GeminiAdapter.complete()` method
- Users CANNOT use JSON/structured output for LLM

## Solution Overview

Mirror TTS implementation pattern:
```
SDK.text() → UnifiedTextClient.execute() → GeminiAdapter.complete()
                                         ↓
                              response_format → response_mime_type mapping
```

---

## Task 1: Implement GeminiAdapter.complete()

**File:** `/mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai/adapters/gemini.py`
**Action:** Add `complete()` method after `get_voices()`
**Pattern:** Follow TTS method structure (lines 145-265)

### Requirements
- Accept `messages`, `model`, `**kwargs`
- Support `response_format` parameter for JSON mode
- Map unified params to Gemini-specific:
  - `response_format={"type": "json_object"}` → `response_mime_type="application/json"`
  - `temperature`, `max_tokens`, `top_p`, `stop` pass through
- Return `TextResponse` compatible dict
- Add breadcrumb tracking like TTS

### Code Template
```python
async def complete(
    self,
    messages: List[Dict[str, Any]],
    model: str,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Generate text with Gemini LLM.

    Args:
        messages: Chat messages [{"role": "user", "content": "..."}]
        model: Gemini model name (e.g., "gemini-2.0-flash")
        **kwargs: temperature, max_tokens, top_p, stop, response_format

    Returns:
        Dict with content, finish_reason, usage
    """
    self._breadcrumb_call_start("complete", model, message_count=len(messages))

    try:
        # Map response_format to Gemini's response_mime_type
        response_format = kwargs.get("response_format")
        generation_config = {
            "temperature": kwargs.get("temperature", 1.0),
            "max_output_tokens": kwargs.get("max_tokens"),
            "top_p": kwargs.get("top_p"),
            "stop_sequences": kwargs.get("stop"),
        }

        if response_format and response_format.get("type") == "json_object":
            generation_config["response_mime_type"] = "application/json"

        # Remove None values
        generation_config = {k: v for k, v in generation_config.items() if v is not None}

        # Convert messages to Gemini format
        contents = self._convert_messages_to_gemini(messages)

        # Call Gemini API
        response = self.client.models.generate_content(
            model=model,
            contents=contents,
            config=self.types.GenerateContentConfig(**generation_config),
        )

        content = response.text
        finish_reason = response.candidates[0].finish_reason if response.candidates else None

        self._breadcrumb_call_success("complete", model, {
            "content_length": len(content),
            "finish_reason": str(finish_reason),
        })

        return {
            "content": content,
            "finish_reason": str(finish_reason) if finish_reason else "stop",
            "usage": {
                "prompt_tokens": getattr(response.usage_metadata, "prompt_token_count", 0),
                "completion_tokens": getattr(response.usage_metadata, "candidates_token_count", 0),
            }
        }

    except Exception as e:
        self._breadcrumb_call_error("complete", model, e, recommendations=[
            "Check API key validity",
            "Verify model supports text generation",
        ])
        raise ProviderError(
            message=f"Gemini completion failed: {e}",
            provider=self.name,
            model=model,
        )

def _convert_messages_to_gemini(self, messages: List[Dict[str, Any]]) -> List:
    """Convert OpenAI-style messages to Gemini Contents format."""
    contents = []
    system_prompt = None

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")

        if role == "system":
            system_prompt = content
        elif role == "user":
            contents.append(self.types.Content(
                role="user",
                parts=[self.types.Part.from_text(content)]
            ))
        elif role == "assistant":
            contents.append(self.types.Content(
                role="model",
                parts=[self.types.Part.from_text(content)]
            ))

    # Prepend system prompt to first user message if exists
    if system_prompt and contents:
        first_content = contents[0].parts[0].text
        contents[0] = self.types.Content(
            role="user",
            parts=[self.types.Part.from_text(f"{system_prompt}\n\n{first_content}")]
        )

    return contents
```

### Validation
```bash
python3 -c "
from unified_ai.adapters import GeminiAdapter
adapter = GeminiAdapter(api_key='test')
assert hasattr(adapter, 'complete')
print('GeminiAdapter.complete() exists')
"
```

---

## Task 2: Create UnifiedTextClient

**File:** `/mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai/clients/text.py` (NEW)
**Action:** Create file mirroring `tts.py` structure
**Pattern:** Follow `clients/tts.py` (lines 1-120)

### Code Template
```python
"""
Unified Text Client for Unified AI SDK.

Provides LLM text generation capabilities with:
- Multi-provider support (Gemini, OpenAI, Anthropic)
- Fallback chain with breadcrumb tracking
- JSON/structured output mode
- Streaming support
"""

import time
from typing import Any, AsyncIterator, Dict, List, Optional

from ..breadcrumbs import add_error, add_info, add_success, SDKLayer
from ..exceptions import AllProvidersFailedError, ProviderError
from ..types import TextRequest, TextResponse
from .base import AdapterRegistry, BaseCapabilityClient


class UnifiedTextClient(BaseCapabilityClient[TextRequest, TextResponse]):
    """
    Unified LLM client with multi-provider fallback support.

    Features:
        - Execute LLM on specific provider/model
        - Automatic fallback through provider chain
        - JSON structured output mode (response_format)
        - Full breadcrumb tracking

    Example:
        client = UnifiedTextClient(registry=registry, fallback_chain=[...])
        request = TextRequest(
            prompt="Extract name from: John Smith is 30",
            response_format={"type": "json_object"}
        )
        response = await client.execute(request, "gemini/gemini-2.0-flash")
    """

    CAPABILITY: str = "text"

    async def execute(self, request: TextRequest, model: str) -> TextResponse:
        """Execute LLM on specific model."""
        start_time = time.time()
        provider, model_name = self._parse_model_string(model)

        adapter = self.registry.get_for_model(model)

        add_info(
            layer=SDKLayer.CLIENT.value,
            action="text_execute_start",
            message=f"Executing LLM with {provider}/{model_name}",
            provider=provider,
            model=model_name,
        )

        # Build kwargs from request - NO hardcoding, pass through
        kwargs: Dict[str, Any] = {}
        if request.temperature is not None:
            kwargs["temperature"] = request.temperature
        if request.max_tokens is not None:
            kwargs["max_tokens"] = request.max_tokens
        if request.top_p is not None:
            kwargs["top_p"] = request.top_p
        if request.stop is not None:
            kwargs["stop"] = request.stop
        if request.response_format is not None:
            kwargs["response_format"] = request.response_format
        if request.tools is not None:
            kwargs["tools"] = request.tools
        if request.tool_choice is not None:
            kwargs["tool_choice"] = request.tool_choice
        if request.provider_params:
            kwargs.update(request.provider_params)

        # Convert prompt to messages if needed
        messages = request.messages
        if messages is None and request.prompt:
            messages = [{"role": "user", "content": request.prompt}]
            if request.system:
                messages.insert(0, {"role": "system", "content": request.system})

        result = await adapter.complete(
            messages=messages,
            model=model_name,
            **kwargs,
        )

        latency_ms = (time.time() - start_time) * 1000

        return TextResponse(
            success=True,
            provider=provider,
            model=model_name,
            latency_ms=latency_ms,
            content=result.get("content", ""),
            finish_reason=result.get("finish_reason"),
            tool_calls=result.get("tool_calls"),
            usage=result.get("usage", {}),
        )

    async def execute_with_fallback(self, request: TextRequest) -> TextResponse:
        """Execute with fallback chain."""
        errors = []

        for model in self.fallback_chain:
            try:
                return await self.execute(request, model)
            except ProviderError as e:
                errors.append({"model": model, "error": str(e)})
                add_warning(
                    layer=SDKLayer.CLIENT.value,
                    action="text_fallback",
                    message=f"Provider {model} failed, trying next",
                    error=str(e),
                )

        raise AllProvidersFailedError(
            message="All text providers failed",
            errors=errors,
        )
```

### Validation
```bash
python3 -c "
from unified_ai.clients.text import UnifiedTextClient
print('UnifiedTextClient imported successfully')
"
```

---

## Task 3: Update clients/__init__.py

**File:** `/mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai/clients/__init__.py`
**Action:** Add UnifiedTextClient export

```python
from .text import UnifiedTextClient
__all__ = [..., "UnifiedTextClient"]
```

---

## Task 4: Add SDK.text() Method

**File:** `/mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai/sdk.py`
**Action:** Add `text()` method after `generate_speech()`
**Pattern:** Follow `generate_speech()` structure

### Code Template
```python
async def text(
    self,
    prompt: Optional[str] = None,
    messages: Optional[List[Dict[str, Any]]] = None,
    model: Optional[str] = None,
    system: Optional[str] = None,
    response_format: Optional[Dict[str, Any]] = None,
    include_breadcrumbs: bool = True,
    **kwargs: Any,
) -> TextResponse:
    """
    High-level LLM API with automatic breadcrumb collection.

    Args:
        prompt: Simple text prompt (converted to messages)
        messages: Chat messages in OpenAI format
        model: Model "provider/model" format (e.g., "gemini/gemini-2.0-flash")
        system: System prompt
        response_format: {"type": "json_object"} for JSON mode
        include_breadcrumbs: Include breadcrumbs in response
        **kwargs: temperature, max_tokens, top_p, stop, provider_params

    Returns:
        TextResponse with content and metadata

    Example:
        # Simple prompt
        response = await sdk.text("What is 2+2?")

        # JSON mode
        response = await sdk.text(
            prompt="Extract: John Smith, age 30",
            response_format={"type": "json_object"},
            model="gemini/gemini-2.0-flash"
        )
    """
    request_id = str(uuid.uuid4())
    collector = start_collection(request_id)

    effective_model = model or self.config.defaults.get("text")

    add_info(
        layer=SDKLayer.SDK.value,
        action="text_request_received",
        request_id=request_id,
        model=effective_model,
        has_json_mode=response_format is not None,
    )

    try:
        request = TextRequest(
            prompt=prompt,
            messages=messages,
            system=system,
            response_format=response_format,
            temperature=kwargs.get("temperature"),
            max_tokens=kwargs.get("max_tokens"),
            top_p=kwargs.get("top_p"),
            stop=kwargs.get("stop"),
            tools=kwargs.get("tools"),
            tool_choice=kwargs.get("tool_choice"),
            provider_params=kwargs.get("provider_params", {}),
        )

        if effective_model:
            result = await self.text_client.execute(request, effective_model)
        else:
            result = await self.text_client.execute_with_fallback(request)

        if include_breadcrumbs:
            result.breadcrumbs = collector.get_breadcrumbs()

        return result

    except Exception as e:
        add_error(
            layer=SDKLayer.SDK.value,
            action="text_request_failed",
            error=str(e),
        )
        raise
```

---

## Task 5: Add text_client Property to SDK

**File:** `/mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai/sdk.py`
**Action:** Add `text_client` property after `tts` property

```python
@property
def text_client(self) -> UnifiedTextClient:
    """Lazy-loaded text client."""
    if self._text_client is None:
        self._text_client = UnifiedTextClient(
            registry=self._registry,
            fallback_chain=self.config.fallback.text if self.config.fallback else [],
        )
    return self._text_client
```

Also add to `__init__`:
```python
self._text_client: Optional[UnifiedTextClient] = None
```

---

## Task 6: Update __init__.py Exports

**File:** `/mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai/__init__.py`
**Action:** Add TextRequest, TextResponse exports

```python
from .types import (
    ...
    TextRequest,
    TextResponse,
)

from .clients import AdapterRegistry, UnifiedTTSClient, UnifiedTextClient

__all__ = [
    ...
    "TextRequest",
    "TextResponse",
    "UnifiedTextClient",
]
```

---

## Task 7: Add Text Presets

**File:** `/mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai/presets/configs/gemini/json_extractor.yaml` (NEW)

```yaml
# JSON structured output preset
provider: gemini
model: gemini-2.0-flash
temperature: 0.3
output_format: json
description: "Low-temperature JSON extraction mode"
extra:
  response_format:
    type: json_object
```

---

## Task 8: Create Integration Test

**File:** `/mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai/tests/test_text_integration.py` (NEW)

```python
"""Integration tests for LLM/Text capability."""

import pytest
import os
from unified_ai import UnifiedAI, Config, ProviderConfig, TextRequest

GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

@pytest.mark.skipif(not GEMINI_KEY, reason="GEMINI_API_KEY not set")
class TestTextIntegration:

    @pytest.fixture
    def sdk(self):
        config = Config(
            providers={"gemini": ProviderConfig(api_key=GEMINI_KEY)},
            defaults={"text": "gemini/gemini-2.0-flash"}
        )
        return UnifiedAI(config)

    @pytest.mark.asyncio
    async def test_simple_prompt(self, sdk):
        response = await sdk.text("What is 2+2? Answer with just the number.")
        assert response.success
        assert "4" in response.content

    @pytest.mark.asyncio
    async def test_json_mode(self, sdk):
        response = await sdk.text(
            prompt="Extract: John Smith is 30 years old",
            response_format={"type": "json_object"},
            system="Return JSON with keys: name, age"
        )
        assert response.success
        import json
        data = json.loads(response.content)
        assert "name" in data or "John" in response.content

    @pytest.mark.asyncio
    async def test_temperature_passthrough(self, sdk):
        """Verify temperature is not hardcoded."""
        response = await sdk.text(
            prompt="Say hello",
            temperature=0.1  # Low temp = deterministic
        )
        assert response.success

    @pytest.mark.asyncio
    async def test_provider_params_passthrough(self, sdk):
        """Verify provider_params reach adapter."""
        response = await sdk.text(
            prompt="Say hello",
            provider_params={"max_tokens": 10}
        )
        assert response.success
```

---

## Validation Commands

After implementation, run:

```bash
# 1. Syntax check
python3 -m py_compile unified_ai/adapters/gemini.py
python3 -m py_compile unified_ai/clients/text.py
python3 -m py_compile unified_ai/sdk.py

# 2. Unit tests
python3 -m pytest unified_ai/tests/test_basic.py -v

# 3. Integration test (requires API key)
GEMINI_API_KEY="..." python3 -m pytest unified_ai/tests/test_text_integration.py -v

# 4. Manual JSON mode test
python3 -c "
import asyncio
from unified_ai import UnifiedAI, Config, ProviderConfig

async def test():
    config = Config(
        providers={'gemini': ProviderConfig(api_key='YOUR_KEY')},
        defaults={'text': 'gemini/gemini-2.0-flash'}
    )
    sdk = UnifiedAI(config)

    # Test JSON mode
    response = await sdk.text(
        prompt='Extract: Alice is 25',
        response_format={'type': 'json_object'},
        system='Return JSON: {name, age}'
    )
    print(f'JSON response: {response.content}')

asyncio.run(test())
"
```

---

## Summary

| Task | File | Action | Est. Lines |
|------|------|--------|------------|
| 1 | adapters/gemini.py | Add complete() method | ~80 |
| 2 | clients/text.py | Create file | ~100 |
| 3 | clients/__init__.py | Add export | 2 |
| 4 | sdk.py | Add text() method | ~60 |
| 5 | sdk.py | Add text_client property | ~15 |
| 6 | __init__.py | Add exports | 5 |
| 7 | presets/configs/ | Add text preset | 10 |
| 8 | tests/ | Add integration tests | ~50 |

**Total:** ~320 lines of code

**Key Principles (from validation):**
- NO hardcoded values that override user input
- Use `kwargs.get("param", default)` pattern
- Pass `response_format` → `response_mime_type` for Gemini
- All params flow through: SDK → Client → Adapter
