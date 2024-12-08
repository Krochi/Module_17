from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.backend.db_depends import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas import CreateTask, UpdateTask
from slugify import slugify
from sqlalchemy import select, insert, update, delete

router = APIRouter()

@router.get("/", response_model=List[CreateTask])
async def all_task(db: Session = Depends(get_db)):
    task = db.scalars(select(Task)).all()
    return task

@router.get("/{task_id}")
async def task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task:
        return task
    raise HTTPException(status_code=404, detail="Task was not found")

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_task(task_data: CreateTask, db: Session = Depends(get_db)):
    # Поиск пользователя
    user = db.scalar(select(User).where(User.id == task_data.user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User was not found")

    # Генерация slug
    slug = slugify(task_data.title)

    task = Task(**task_data.dict(), slug=slug) #, user_id=task_data.user_id)

    db.add(task)
    db.commit()
    db.refresh(task)

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful",
        "task": task
    }

@router.put("/update/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    task_data: UpdateTask,
    db: Session = Depends(get_db)
):
    stmt = update(Task).where(Task.id == task_id).values(**task_data.dict())
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}

@router.delete("/delete/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    stmt = delete(Task).where(Task.id == task_id)
    result = db.execute(stmt)
    db.commit()
    if result.rowcount:
        return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion is successful!"}
    raise HTTPException(status_code=404, detail="Task was not found")
