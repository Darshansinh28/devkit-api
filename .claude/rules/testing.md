---
paths: tests/**/*.py
---

# Testing

- Use `fastapi.testclient.TestClient` against `app.main:app`
- Clear `store` collections in `setup_function` so tests stay isolated
- Cover happy path + auth failure for every new resource
- Run `pytest -q` before claiming done
- Prefer one flow test that registers → logs in → exercises CRUD
