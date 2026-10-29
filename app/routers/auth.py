from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import Token, UserCreate, UserLogin, UserOut
from app.services.security import create_access_token, hash_password, verify_password
from app.store import store

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate) -> UserOut:
    try:
        user = store.create_user(payload.email, hash_password(payload.password))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return UserOut(id=user.id, email=user.email, created_at=user.created_at)


@router.post("/login", response_model=Token)
def login(payload: UserLogin) -> Token:
    user = store.get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return Token(access_token=create_access_token(user.id))
