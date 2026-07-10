from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate

tasks = []
task_id_counter = 1

def create_task(db: Session, task_data: TaskCreate) -> Task:
    new_task = Task(
        title=task_data.title,
        description=task_data.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

def get_all_tasks(db: Session) -> list[Task]:
    return db.query(Task).all()

def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id).first()