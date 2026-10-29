from pydantic import BaseModel, Field


class AISummarizeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=50_000)
    max_bullets: int = Field(default=5, ge=1, le=12)


class AISummarizeResponse(BaseModel):
    summary: str
    bullets: list[str]
    mode: str  # "live" | "mock"
