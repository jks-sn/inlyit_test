from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.utils.get_db import get_db

router = APIRouter()

@router.post("/", response_model=schemas.User)
async def create_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    user = await crud.user.create(db=db, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.user.get(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int, user_in: schemas.UserUpdate, db: AsyncSession = Depends(get_db)
):
    user = await crud.user.get(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user = await crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await crud.user.get(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await crud.user.remove(db=db, db_obj=user)
    return {"detail": "User deleted"}

@router.get("/", response_model=List[schemas.User])
async def read_users(db: AsyncSession = Depends(get_db)):
    users = await crud.user.get_multi(db=db)
    return users
