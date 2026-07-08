from fastapi import APIRouter

from app.schemas.task import TaskCreate
from app.services.task_service import (create_task, get_all_tasks)

router = APIRouter()

@router.post("/tasks")
def add_task(task: TaskCreate):
    return create_task(task)

@router.get("/tasks")
def get_tasks():
    return get_all_tasks()