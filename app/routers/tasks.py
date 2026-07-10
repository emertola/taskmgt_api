from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskResponse
from app.services.task_service import (create_task, get_all_tasks)

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskResponse, status_code=201)
def add_task(task: TaskCreate, db: Annotated[Session, Depends(get_db)]):
    return create_task(db, task)

@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Annotated[Session, Depends(get_db)]):
    return get_all_tasks(db)