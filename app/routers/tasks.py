from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import (create_task, delete_task, get_all_tasks, get_task_by_id, update_task)

router = APIRouter(prefix="/tasks", tags=["tasks"])
TASK_NOT_FOUND_DETAIL = "Task not found"

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
            detail=TASK_NOT_FOUND_DETAIL,
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def edit_task(task_id: int, task_data: TaskUpdate, db: Annotated[Session, Depends(get_db)]):
    updated = update_task(db, task_id, task_data)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TASK_NOT_FOUND_DETAIL,
        )
    return updated

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def remove_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    was_deleted = delete_task(db, task_id)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=TASK_NOT_FOUND_DETAIL,
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)