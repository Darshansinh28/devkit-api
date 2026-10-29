---
paths: app/services/security.py, app/deps.py, app/routers/auth.py, app/config.py
---

# Security

- Passwords: hash with passlib bcrypt — never store plaintext
- Tokens: JWT via `create_access_token` / `decode_access_token`
- `SECRET_KEY` comes from env; default is for local only
- Do not log tokens, passwords, or API keys
- AI live mode only when `OPENAI_API_KEY` is set; otherwise mock
- Reject unauthenticated access to notes, tasks, and AI routes
