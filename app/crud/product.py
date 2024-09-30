from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.model.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class CRUDProduct:
    async def create(self, db: AsyncSession, obj_in: ProductCreate):
        product = Product(**obj_in.dict())
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    async def get(self, db: AsyncSession, product_id: int):
        result = await db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, db_obj: Product, obj_in: ProductUpdate):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, db_obj: Product):
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def get_multi(self, db: AsyncSession):
        result = await db.execute(select(Product))
        return result.scalars().all()

product = CRUDProduct()
