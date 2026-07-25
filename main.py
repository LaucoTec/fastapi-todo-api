from fastapi import FastAPI, HTTPException

examples = {
    1: {
        "id": 1,
        "title": "Task 1",
        "description": "This is an example task",
        "completed": False,
    },
    2: {
        "id": 2,
        "title": "Task 2",
        "description": "This is another example task",
        "completed": False,
    },
    3: {
        "id": 3,
        "title": "Task 3",
        "description": "This is yet another example task",
        "completed": False,
    },
}

app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/tasks")
async def get_tasks():
    return list(examples.values())


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    task = examples.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    return task


@app.post("/tasks", status_code=201)
async def create_task(task: dict):
    if "title" not in task or "description" not in task:
        raise HTTPException(
            status_code=400, detail="Task must have a title and description"
        )

    task_id = max(examples.keys()) + 1
    task["id"] = task_id
    task["completed"] = False
    examples[task_id] = task
    return task


@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}
