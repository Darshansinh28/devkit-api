from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app.schemas.ai import AISummarizeRequest, AISummarizeResponse
from app.services.ai import summarize_text
from app.store.memory import UserRecord

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/summarize", response_model=AISummarizeResponse)
async def summarize(
    payload: AISummarizeRequest,
    user: UserRecord = Depends(get_current_user),
) -> AISummarizeResponse:
    _ = user  # auth required; keeps AI behind login like a real product
    return await summarize_text(payload.text, payload.max_bullets)
