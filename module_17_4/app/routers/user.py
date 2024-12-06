from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.backend.db_depends import get_db
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
from slugify import slugify
from sqlalchemy import select, insert, update, delete

router = APIRouter()

@router.get("/", response_model=List[CreateUser])
async def all_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()
    return users

@router.get("/{user_id}")
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.id == user_id))
    if user:
        return user
    raise HTTPException(status_code=404, detail="User was not found")


@router.post("/users/create", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: CreateUser, db: Session = Depends(get_db)):
    # Генерация slug
    slug = slugify(user_data.username)


    user = User(**user_data.dict(), slug=slug)


    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "status_code": status.HTTP_201_CREATED,
        "transaction": "Successful",
        "user": user
    }


# @router.post("/create", status_code=status.HTTP_201_CREATED)
# async def create_user(user: CreateUser, db: Session = Depends(get_db)):
#     slug = slugify(user.username)
#     stmt = insert(User).values(**user.dict(), slug=slug)
#     db.execute(stmt)
#     db.commit()
#     return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

# @router.put("/update/{user_id}")
# async def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
#     stmt = update(User).where(User.id == user_id).values(**user.dict())
#     result = db.execute(stmt)
#     db.commit()
#     if result.rowcount:
#         return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}
#     raise HTTPException(status_code=404, detail="User was not found")

@router.put("/update/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_id: int,
    user_data: UpdateUser,
    db: Session = Depends(get_db)
):
    stmt = update(User).where(User.id == user_id).values(**user_data.dict())
    result = db.execute(stmt)
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    db.commit()
    if result.rowcount:
        return {"status_code": status.HTTP_200_OK, "transaction": "User deletion is successful!"}
    raise HTTPException(status_code=404, detail="User was not found")
