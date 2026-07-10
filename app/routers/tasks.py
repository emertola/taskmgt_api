from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import (create_task, get_all_tasks, get_task_by_id)

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def add_task(task: TaskCreate, db: Annotated[Session, Depends(get_db)]):
    return create_task(db, task)

@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Annotated[Session, Depends(get_db)]):
    return get_all_tasks(db)

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Annotated[Session, Depends(get_db)],
):
    task = get_task_by_id(db, task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task