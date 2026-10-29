# devkit-api

Local FastAPI developer kit (auth, notes, tasks, optional AI summarize). Public reference project — keep it clean, documented, and easy to extend with Claude Code.

See @README.md for quick start and example curls.

## Commands

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
pytest -q
```

Docs: http://127.0.0.1:8000/docs

## Layout

| Path | Role |
|------|------|
| `app/main.py` | FastAPI app + router wiring |
| `app/config.py` | Settings via pydantic-settings |
| `app/deps.py` | Auth dependency (`get_current_user`) |
| `app/routers/` | HTTP routes by domain |
| `app/schemas/` | Pydantic request/response models |
| `app/services/` | Business logic (security, AI) |
| `app/store/` | In-memory store (swap later for DB) |
| `tests/` | API tests with TestClient |

## Conventions

- Prefer small routers + schemas + services; do not dump logic into `main.py`
- New resources need: schema → store methods → router → tests
- Protected routes use `Depends(get_current_user)`
- AI features must work in **mock mode** when `OPENAI_API_KEY` is unset
- Never commit `.env`, secrets, or real API keys
- Keep README + CLAUDE.md in sync when commands or layout change

## Do not

- Copy private JobAgent / org product code into this repo
- Add heavy frameworks without a clear need
- Break mock-mode AI fallbacks

## Skills

- `/add-endpoint` — scaffold a new authenticated resource
- `/verify` — install (if needed), run tests, sanity-check health
