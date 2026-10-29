---
name: extend-ai
description: Add a new AI assist endpoint under /ai that supports live OpenAI-compatible calls and mock fallback. Use when adding summarize/review/rewrite style features.
---

# Extend AI

## Rules

- New route under `app/routers/ai.py` (or a dedicated router if it grows)
- Request/response schemas in `app/schemas/ai.py`
- Implementation in `app/services/ai.py`
- **Must** work without `OPENAI_API_KEY` (mock mode)
- Live mode: OpenAI-compatible `chat/completions` via httpx; on failure fall back to mock
- Require auth (`get_current_user`)
- Add/adjust tests asserting `mode == "mock"` without a key

## Checklist

- [ ] Mock path works offline
- [ ] Live path only when key present
- [ ] No API keys in logs or fixtures
- [ ] `pytest -q` passes
