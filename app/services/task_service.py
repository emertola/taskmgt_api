from app.schemas.task import TaskCreate, TaskResponse

tasks = []
task_id_counter = 1

def create_task(task: TaskCreate):
    global task_id_counter
    new_task = TaskResponse(
        id=task_id_counter,
        title=task.title,
        description=task.description,
        completed=False
    )
    task_id_counter += 1
    tasks.append(new_task)
    return new_task

def get_all_tasks():
    return tasks