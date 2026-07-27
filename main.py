from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator


class Task(BaseModel):
    id: int | None = None
    title: str
    description: str
    completed: bool = False


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None

    @model_validator(mode="before")
    def check_empty(cls, values):
        if not values:
            raise ValueError("At least one field must be provided.")
        return values


examples = {
    1: Task(
        id=1, title="Task 1", description="This is an example task", completed=False
    ),
    2: Task(
        id=2,
        title="Task 2",
        description="This is another example task",
        completed=False,
    ),
    3: Task(
        id=3,
        title="Task 3",
        description="This is yet another example task",
        completed=False,
    ),
}

app = FastAPI()


@app.get("/health", summary="Health Check", description="Check the health of the API")
async def health_check():
    return {"status": "ok"}


@app.get("/stats", summary="Statistics", description="Get statistics about the tasks")
async def get_stats():
    total_tasks = len(examples)
    completed_tasks = sum(1 for task in examples.values() if task.completed)
    return {"total_tasks": total_tasks, "completed_tasks": completed_tasks}


@app.get(
    "/tasks",
    response_model=list[Task],
    summary="Get All Tasks",
    description="Retrieve a list of all tasks",
)
async def get_tasks():
    return list(examples.values())


@app.get(
    "/tasks/{task_id}",
    response_model=Task,
    summary="Get Task",
    description="Retrieve a specific task by its ID",
)
async def get_task(task_id: int):
    task = examples.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return task


@app.post(
    "/tasks",
    status_code=201,
    response_model=Task,
    summary="Create Task",
    description="Create a new task",
)
async def create_task(task: TaskCreate):

    task_id = max(examples.keys()) + 1
    new_task = Task(id=task_id, title=task.title, description=task.description)
    examples[task_id] = new_task
    return new_task


@app.put(
    "/tasks/{task_id}",
    response_model=Task,
    summary="Update Task",
    description="Update an existing task",
)
async def update_task(task_id: int, updated_task: TaskUpdate):
    task = examples.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")

    for field, value in updated_task.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    examples[task_id] = task
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=204,
    summary="Delete Task",
    description="Delete an existing task",
)
async def delete_task(task_id: int):
    task = examples.pop(task_id, None)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")


@app.get("/", summary="Root Endpoint", description="Get information about the API")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}
