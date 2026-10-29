---
name: verify
description: Run pytest and smoke-check health for devkit-api before claiming done.
---

# Verify

```bash
source .venv/bin/activate 2>/dev/null || (python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt)
pytest -q
```

Done when tests pass and no secrets were printed.
