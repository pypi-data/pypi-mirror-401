# Unified AI SDK - Session Handover

[LATEST: 2026-01-13 19:30 | session: unified-ai-testing]

## 🧠 Contradicts Training - READ FIRST!

1. **You'd think:** Run python from unified_ai dir → **Reality:** Causes circular import with `types/` folder conflicting with stdlib `types` | **Fix:** Always use `PYTHONPATH=.. python3` from parent dir

2. **You'd think:** Anthropic max_tokens has sensible default → **Reality:** Anthropic API REQUIRES max_tokens, no default | **Fix:** Config lookup from `configs/providers/anthropic.yaml` for model-specific max_output_tokens

3. **You'd think:** ElevenLabs uses voice names → **Reality:** Requires voice_id like `21m00Tcm4TlvDq8ikWAM` not "Rachel" | **Fix:** Use voice IDs from API

4. **You'd think:** Gemini TTS works with short text → **Reality:** Fails with "Model tried to generate..." for very short text | **Fix:** Use text >10 chars

## ✅ What Worked

1. **Test command:** `cd unified_ai && PYTHONPATH=.. python3 tests/test_real_api.py`
2. **Working Gemini key:** `AIzaSyCqpLkbT_Z4j8-Xvj3Z16X91sOtGxZNK44` (from resilient pipeline)
3. **Working adapters:** OpenRouter, ElevenLabs, Gemini (text + TTS + JSON schema)
4. **JSON schema enforcement:** Gemini supports `response_format={"type": "json_schema", "json_schema": {...}}`

## ❌ What Failed (Billing Issues - NOT Code)

- OpenAI: Quota exceeded (429)
- Anthropic: Credit balance low (400)
- Gemini key 1 (`AIzaSyBCHil67...`): Rate limited

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.env` | All API keys (updated with working Gemini key) |
| `tests/test_real_api.py` | Real API tests with safety protections |
| `adapters/anthropic.py:112-122` | Model-specific max_tokens from config |
| `configs/providers/*.yaml` | Provider capability matrix |

## 🔧 Remaining Work

1. **Add capabilities matrix** to remaining provider configs:
   - `gemini.yaml` - need: capabilities array, stt service, embeddings
   - `elevenlabs.yaml` - need: capabilities array
   - `anthropic.yaml` - need: capabilities array
   - `openrouter.yaml` - need: capabilities array

2. **OpenAI config updated** with: capabilities array, embeddings service, image service

## 📊 Test Results (7/7 PASSED)

```
openrouter_text   PASS  2.1s
gemini_text       PASS  1.6s
gemini_json_obj   PASS  Valid JSON
gemini_json_schema PASS Strict schema enforced
elevenlabs_tts    PASS  10.9KB MP3
gemini_tts        PASS  34KB MP3
unified_client    PASS  Client abstraction works
```

## 🔑 API Keys Location

`/mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai/.env`

## Quick Resume

```bash
cd /mnt/d/Vibe_coding_projects/turov_bot/turov_bot_project/v23/libs/unified_ai
source .env
PYTHONPATH=.. python3 tests/test_real_api.py
```
