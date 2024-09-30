from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.model.cart_item import CartItem
from app.schemas.cart_item import CartItemCreate, CartItemUpdate

class CRUDCartItem:
    async def create(self, db: AsyncSession, obj_in: CartItemCreate):
        cart_item = CartItem(**obj_in.dict())
        db.add(cart_item)
        await db.commit()
        await db.refresh(cart_item)
        return cart_item

    async def get(self, db: AsyncSession, item_id: int):
        result = await db.execute(select(CartItem).where(CartItem.id == item_id))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, db_obj: CartItem, obj_in: CartItemUpdate):
        db_obj.quantity = obj_in.quantity
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, db_obj: CartItem):
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def get_multi_by_user(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(CartItem).where(CartItem.user_id == user_id))
        return result.scalars().all()

cart_item = CRUDCartItem()
