from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_current_user
from app.schemas.tasks import TaskCreate, TaskOut, TaskUpdate
from app.store import store
from app.store.memory import UserRecord

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskOut])
def list_tasks(user: UserRecord = Depends(get_current_user)) -> list[TaskOut]:
    return [
        TaskOut(
            id=t.id,
            title=t.title,
            done=t.done,
            created_at=t.created_at,
            updated_at=t.updated_at,
        )
        for t in store.list_tasks(user.id)
    ]


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, user: UserRecord = Depends(get_current_user)) -> TaskOut:
    task = store.create_task(user.id, payload.title)
    return TaskOut(
        id=task.id,
        title=task.title,
        done=task.done,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.patch("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    user: UserRecord = Depends(get_current_user),
) -> TaskOut:
    task = store.update_task(user.id, task_id, title=payload.title, done=payload.done)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskOut(
        id=task.id,
        title=task.title,
        done=task.done,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, user: UserRecord = Depends(get_current_user)) -> None:
    if not store.delete_task(user.id, task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
