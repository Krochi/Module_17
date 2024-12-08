from fastapi import FastAPI
from app.routers import user, task

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
