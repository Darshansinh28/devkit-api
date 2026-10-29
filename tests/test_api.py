from fastapi.testclient import TestClient

from app.main import app
from app.store import store

client = TestClient(app)


def setup_function() -> None:
    store.users.clear()
    store.users_by_email.clear()
    store.notes.clear()
    store.tasks.clear()


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["ai_mode"] == "mock"


def test_auth_notes_tasks_ai_flow() -> None:
    register = client.post(
        "/auth/register",
        json={"email": "dev@example.com", "password": "password123"},
    )
    assert register.status_code == 201

    login = client.post(
        "/auth/login",
        json={"email": "dev@example.com", "password": "password123"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    note = client.post(
        "/notes",
        headers=headers,
        json={"title": "Ship checklist", "body": "Write tests. Push to GitHub. Submit Alignerr."},
    )
    assert note.status_code == 201
    note_id = note.json()["id"]

    notes = client.get("/notes", headers=headers)
    assert notes.status_code == 200
    assert len(notes.json()) == 1

    task = client.post("/tasks", headers=headers, json={"title": "Finish survey"})
    assert task.status_code == 201
    task_id = task.json()["id"]

    done = client.patch(f"/tasks/{task_id}", headers=headers, json={"done": True})
    assert done.status_code == 200
    assert done.json()["done"] is True

    summary = client.post(
        "/ai/summarize",
        headers=headers,
        json={
            "text": "devkit-api is a local FastAPI kit. It has auth, notes, tasks, and AI summarize.",
            "max_bullets": 3,
        },
    )
    assert summary.status_code == 200
    body = summary.json()
    assert body["mode"] == "mock"
    assert body["summary"]
    assert isinstance(body["bullets"], list)

    deleted = client.delete(f"/notes/{note_id}", headers=headers)
    assert deleted.status_code == 204


def test_notes_require_auth() -> None:
    response = client.get("/notes")
    assert response.status_code == 401
