"""In-memory store for local demos — swap for Postgres/SQLite later."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from typing import Any
from uuid import uuid4


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class UserRecord:
    id: str
    email: str
    hashed_password: str
    created_at: datetime = field(default_factory=_now)


@dataclass
class NoteRecord:
    id: str
    user_id: str
    title: str
    body: str
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)


@dataclass
class TaskRecord:
    id: str
    user_id: str
    title: str
    done: bool = False
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)


class MemoryStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self.users: dict[str, UserRecord] = {}
        self.users_by_email: dict[str, str] = {}
        self.notes: dict[str, NoteRecord] = {}
        self.tasks: dict[str, TaskRecord] = {}

    def create_user(self, email: str, hashed_password: str) -> UserRecord:
        with self._lock:
            if email.lower() in self.users_by_email:
                raise ValueError("email already registered")
            user = UserRecord(id=str(uuid4()), email=email.lower(), hashed_password=hashed_password)
            self.users[user.id] = user
            self.users_by_email[user.email] = user.id
            return user

    def get_user_by_email(self, email: str) -> UserRecord | None:
        user_id = self.users_by_email.get(email.lower())
        return self.users.get(user_id) if user_id else None

    def get_user(self, user_id: str) -> UserRecord | None:
        return self.users.get(user_id)

    def create_note(self, user_id: str, title: str, body: str) -> NoteRecord:
        note = NoteRecord(id=str(uuid4()), user_id=user_id, title=title, body=body)
        with self._lock:
            self.notes[note.id] = note
        return note

    def list_notes(self, user_id: str) -> list[NoteRecord]:
        return sorted(
            (n for n in self.notes.values() if n.user_id == user_id),
            key=lambda n: n.created_at,
            reverse=True,
        )

    def get_note(self, user_id: str, note_id: str) -> NoteRecord | None:
        note = self.notes.get(note_id)
        if note and note.user_id == user_id:
            return note
        return None

    def update_note(self, user_id: str, note_id: str, **fields: Any) -> NoteRecord | None:
        note = self.get_note(user_id, note_id)
        if not note:
            return None
        with self._lock:
            for key, value in fields.items():
                if value is not None and hasattr(note, key):
                    setattr(note, key, value)
            note.updated_at = _now()
        return note

    def delete_note(self, user_id: str, note_id: str) -> bool:
        note = self.get_note(user_id, note_id)
        if not note:
            return False
        with self._lock:
            del self.notes[note_id]
        return True

    def create_task(self, user_id: str, title: str) -> TaskRecord:
        task = TaskRecord(id=str(uuid4()), user_id=user_id, title=title)
        with self._lock:
            self.tasks[task.id] = task
        return task

    def list_tasks(self, user_id: str) -> list[TaskRecord]:
        return sorted(
            (t for t in self.tasks.values() if t.user_id == user_id),
            key=lambda t: t.created_at,
            reverse=True,
        )

    def get_task(self, user_id: str, task_id: str) -> TaskRecord | None:
        task = self.tasks.get(task_id)
        if task and task.user_id == user_id:
            return task
        return None

    def update_task(self, user_id: str, task_id: str, **fields: Any) -> TaskRecord | None:
        task = self.get_task(user_id, task_id)
        if not task:
            return None
        with self._lock:
            for key, value in fields.items():
                if value is not None and hasattr(task, key):
                    setattr(task, key, value)
            task.updated_at = _now()
        return task

    def delete_task(self, user_id: str, task_id: str) -> bool:
        task = self.get_task(user_id, task_id)
        if not task:
            return False
        with self._lock:
            del self.tasks[task_id]
        return True


store = MemoryStore()
