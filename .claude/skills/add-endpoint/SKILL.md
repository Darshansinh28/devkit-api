---
name: add-endpoint
description: Scaffold a new authenticated FastAPI resource (schema, store, router, tests) in devkit-api. Use when adding a new CRUD API resource or endpoint group.
---

# Add endpoint

## Inputs

Ask for (if not given):

1. Resource name (singular, e.g. `bookmark`)
2. Fields (name + type)
3. Whether auth is required (default: yes)

## Steps

1. Add Pydantic models in `app/schemas/{resource}.py` (`Create`, `Update`, `Out`)
2. Export them from `app/schemas/__init__.py`
3. Add store methods on `MemoryStore` in `app/store/memory.py` (create/list/get/update/delete)
4. Create `app/routers/{resource}s.py` with JWT via `Depends(get_current_user)`
5. `app.include_router(...)` in `app/main.py`
6. Extend `tests/test_api.py` with register → login → CRUD assertions
7. Run `pytest -q` and fix failures

## Checklist

- [ ] Schema + store + router + main wiring
- [ ] Auth on all mutating/list routes
- [ ] Tests pass
- [ ] OpenAPI shows the new tag at `/docs`
