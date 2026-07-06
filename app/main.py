from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Annotated

app = FastAPI()

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False

tasks: List[Task] = []
task_id_counter = 1
notFoundErrorMessage = "Task not found"

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/tasks")
def create_task(task: Task, response_model=Task):
    global task_id_counter

    task.id = task_id_counter
    task_id_counter += 1
    
    tasks.append(task)
    return task


@app.get("/tasks", response_model=List[Task])
def get_tasks(completed: Annotated[Optional[bool], Query(description="Filter by completed status")] = None):
    if completed is None:
        return tasks
    
    filtered_tasks = [task for task in tasks if task.completed == completed]
    return filtered_tasks

@app.get("/tasks/{task_id}", responses={404: {"description": notFoundErrorMessage}})
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail=notFoundErrorMessage)

@app.put("/tasks/{task_id}", response_model=Task, responses={404: {"description": notFoundErrorMessage}})
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            updated_task.id = task_id
            tasks[index] = updated_task
            return updated_task
        
    raise HTTPException(status_code=404, detail=notFoundErrorMessage)

@app.delete("/tasks/{task_id}", responses={404: {"description": notFoundErrorMessage}})
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[index]
            return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail=notFoundErrorMessage)

@app.patch("/tasks/{task_id}/complete", responses={404: {"description": notFoundErrorMessage}})
def complete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.completed = True
            return task
    raise HTTPException(status_code=404, detail=notFoundErrorMessage)

