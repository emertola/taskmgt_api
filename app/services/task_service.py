from app.schemas.task import Task

tasks = []
task_id_counter = 1

def create_task(task: Task):
    global task_id_counter
    task.id = task_id_counter
    task_id_counter += 1
    tasks.append(task)
    return task

def get_all_tasks():
    return tasks