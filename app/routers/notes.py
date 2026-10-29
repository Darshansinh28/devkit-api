from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_current_user
from app.schemas.notes import NoteCreate, NoteOut, NoteUpdate
from app.store import store
from app.store.memory import UserRecord

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteOut])
def list_notes(user: UserRecord = Depends(get_current_user)) -> list[NoteOut]:
    return [
        NoteOut(
            id=n.id,
            title=n.title,
            body=n.body,
            created_at=n.created_at,
            updated_at=n.updated_at,
        )
        for n in store.list_notes(user.id)
    ]


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_note(payload: NoteCreate, user: UserRecord = Depends(get_current_user)) -> NoteOut:
    note = store.create_note(user.id, payload.title, payload.body)
    return NoteOut(
        id=note.id,
        title=note.title,
        body=note.body,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


@router.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: str, user: UserRecord = Depends(get_current_user)) -> NoteOut:
    note = store.get_note(user.id, note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteOut(
        id=note.id,
        title=note.title,
        body=note.body,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


@router.patch("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: str,
    payload: NoteUpdate,
    user: UserRecord = Depends(get_current_user),
) -> NoteOut:
    note = store.update_note(user.id, note_id, title=payload.title, body=payload.body)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return NoteOut(
        id=note.id,
        title=note.title,
        body=note.body,
        created_at=note.created_at,
        updated_at=note.updated_at,
    )


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: str, user: UserRecord = Depends(get_current_user)) -> None:
    if not store.delete_note(user.id, note_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
