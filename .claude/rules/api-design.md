---
paths: app/routers/**/*.py, app/schemas/**/*.py, app/main.py
---

# API design

- One router module per resource (`notes.py`, `tasks.py`, …)
- Prefix routes with `/{resource}` and tag them for OpenAPI
- Use Pydantic models in `app/schemas/` for all request/response bodies
- Return proper status codes: `201` create, `204` delete, `404` missing, `401` auth
- Wire new routers in `app/main.py` with `app.include_router(...)`
- Keep handlers thin — call store/services, do not embed business logic
