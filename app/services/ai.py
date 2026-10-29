from __future__ import annotations

import re

import httpx

from app.config import get_settings
from app.schemas.ai import AISummarizeResponse


def _mock_summarize(text: str, max_bullets: int) -> AISummarizeResponse:
    cleaned = re.sub(r"\s+", " ", text).strip()
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]
    bullets = sentences[:max_bullets] or [cleaned[:180]]
    summary = " ".join(bullets[:2]) if bullets else cleaned[:240]
    return AISummarizeResponse(summary=summary, bullets=bullets, mode="mock")


async def summarize_text(text: str, max_bullets: int) -> AISummarizeResponse:
    settings = get_settings()
    if not settings.openai_api_key:
        return _mock_summarize(text, max_bullets)

    prompt = (
        f"Summarize the text in 1-2 sentences, then give up to {max_bullets} bullet points.\n"
        "Return plain text with a Summary: line and Bullets: list.\n\n"
        f"TEXT:\n{text}"
    )
    url = f"{settings.openai_base_url.rstrip('/')}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": settings.openai_model,
        "messages": [
            {"role": "system", "content": "You are a concise technical writing assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers, json=body)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
    except Exception:
        # Fail soft: never block local workflow on provider errors.
        return _mock_summarize(text, max_bullets)

    bullets = [
        line.lstrip("-•* ").strip()
        for line in content.splitlines()
        if line.strip().startswith(("-", "•", "*"))
    ][:max_bullets]
    if not bullets:
        bullets = [content[:180]]
    return AISummarizeResponse(summary=content.split("\n")[0][:500], bullets=bullets, mode="live")
