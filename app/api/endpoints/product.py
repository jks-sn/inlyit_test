from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, schemas
from app.utils.get_db import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Product)
async def create_product(product_in: schemas.ProductCreate, db: AsyncSession = Depends(get_db)):
    product = await crud.product.create(db=db, obj_in=product_in)
    return product

@router.get("/{product_id}", response_model=schemas.Product)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.product.get(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int, product_in: schemas.ProductUpdate, db: AsyncSession = Depends(get_db)
):
    product = await crud.product.get(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product = await crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await crud.product.get(db=db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    await crud.product.remove(db=db, db_obj=product)
    return {"detail": "Product deleted"}

@router.get("/", response_model=List[schemas.Product])
async def read_products(db: AsyncSession = Depends(get_db)):
    products = await crud.product.get_multi(db=db)
    return products
