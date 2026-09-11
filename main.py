from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Todo API", description="Simple Todo API with in-memory storage")

# In-memory storage
todos: dict[int, dict] = {}
counter: int = 0


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


@app.get("/")
async def root():
    return {"message": "Welcome to the Todo API. Visit /docs for Swagger UI."}


@app.post("/todos", status_code=201)
async def create_todo(todo: TodoCreate):
    global counter
    counter += 1
    todos[counter] = {
        "id": counter,
        "title": todo.title,
        "description": todo.description,
        "completed": False,
    }
    return todos[counter]


@app.get("/todos")
async def get_all_todos():
    return list(todos.values())


@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]


@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, todo: TodoUpdate):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    existing = todos[todo_id]
    if todo.title is not None:
        existing["title"] = todo.title
    if todo.description is not None:
        existing["description"] = todo.description
    if todo.completed is not None:
        existing["completed"] = todo.completed
    return existing


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    deleted = todos.pop(todo_id)
    return {"message": "Todo deleted", "todo": deleted}