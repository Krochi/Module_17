from fastapi import FastAPI
from .routers import task, user
from backend.db import engine, Base
from sqlalchemy.schema import CreateTable
from models import User, Task

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)

print(CreateTable(User.__table__))
print(CreateTable(Task.__table__))