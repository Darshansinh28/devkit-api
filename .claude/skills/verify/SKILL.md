---
name: verify
description: Install deps if needed, run pytest, and smoke-check /health for devkit-api. Use before commits, PRs, or claiming a feature is done.
---

# Verify

## Steps

```bash
source .venv/bin/activate 2>/dev/null || (python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt)
pytest -q
```

Optional smoke (if server not already running):

```bash
uvicorn app.main:app --port 8000 &
sleep 1
curl -s http://127.0.0.1:8000/health
kill %1 2>/dev/null || true
```

## Done when

- `pytest -q` exits 0
- `/health` returns `"status": "ok"` when checked
- No secrets were printed
