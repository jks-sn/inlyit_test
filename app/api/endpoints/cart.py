from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.db.session import AsyncSessionLocal
from app.utils.get_db import get_db

router = APIRouter()

@router.post("/items/", response_model=schemas.CartItem)
async def add_item_to_cart(
    item: schemas.CartItemCreate, db: AsyncSession = Depends(get_db)
):
    cart_item = await crud.cart_item.create(db=db, obj_in=item)
    return cart_item

@router.delete("/items/{item_id}")
async def delete_item_from_cart(item_id: int, db: AsyncSession = Depends(get_db)):
    cart_item = await crud.cart_item.get(db=db, item_id=item_id)
    if cart_item is None:
        raise HTTPException(status_code=404, detail="CartItem not found")
    await crud.cart_item.remove(db=db, db_obj=cart_item)
    return {"detail": "Item deleted"}

@router.put("/items/{item_id}", response_model=schemas.CartItem)
async def update_item_quantity(
    item_id: int, item: schemas.CartItemUpdate, db: AsyncSession = Depends(get_db)
):
    cart_item = await crud.cart_item.get(db=db, item_id=item_id)
    if cart_item is None:
        raise HTTPException(status_code=404, detail="CartItem not found")
    cart_item = await crud.cart_item.update(db=db, db_obj=cart_item, obj_in=item)
    return cart_item

@router.get("/items/", response_model=List[schemas.CartItem])
async def get_cart_items(user_id: int, db: AsyncSession = Depends(get_db)):
    cart_items = await crud.cart_item.get_multi_by_user(db=db, user_id=user_id)
    return cart_items
