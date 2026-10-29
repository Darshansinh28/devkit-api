# devkit-api

Local developer API kit built with AI coding assistants (**Claude Code / Cursor**).

A small but real FastAPI backend you can run on `localhost:8000`, extend feature-by-feature, and use as a public reference project.

## Features

| Area | Endpoints |
|------|-----------|
| Health | `GET /health` |
| Auth | `POST /auth/register`, `POST /auth/login` |
| Notes | CRUD under `/notes` (JWT required) |
| Tasks | create / list / update / delete under `/tasks` |
| AI | `POST /ai/summarize` — live if `OPENAI_API_KEY` is set, otherwise **mock mode** |

Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Why this project

- Public, self-contained, no private product IP
- Feels like a real product API (auth + resources + AI assist)
- Designed to be iteratively extended with Claude Code (new routes, persistence, admin, webhooks)

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

### Docker

```bash
cp .env.example .env
docker compose up --build
```

## Example flow

```bash
# register + login
curl -s -X POST http://127.0.0.1:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","password":"password123"}'

TOKEN=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"you@example.com","password":"password123"}' | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')

# create a note
curl -s -X POST http://127.0.0.1:8000/notes \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"title":"Ideas","body":"Add SQLite next. Then a React client."}'

# AI summarize (mock without API key)
curl -s -X POST http://127.0.0.1:8000/ai/summarize \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"text":"Ship the API. Add tests. Keep building with Claude Code.","max_bullets":3}'
```

## Tests

```bash
pytest -q
```

## Roadmap (good Claude Code sessions)

- [ ] SQLite / Postgres persistence
- [ ] Refresh tokens + password reset
- [ ] `/ai/review` for code-diff review
- [ ] Minimal React client
- [ ] Rate limiting + request logging

## Claude Code / Cursor setup

This repo is initialized for AI coding assistants:

| Path | Purpose |
|------|---------|
| `CLAUDE.md` | Always-on project instructions for Claude Code |
| `.claude/rules/` | Path-scoped rules (API, testing, security) |
| `.claude/skills/` | `/add-endpoint`, `/verify`, `/extend-ai` |
| `.claude/settings.json` | Safe local command permissions |
| `.cursor/rules/` | Cursor always-on + Python API rules |
| `.cursor/skills/` | Cursor mirrors of key skills |

In Claude Code: open this folder, then use `/add-endpoint` or `/verify`. Check loaded memory with `/context`.

## License

MIT

