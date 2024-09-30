from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.model.user import User
from app.schemas.user import UserCreate, UserUpdate

class CRUDUser:
    async def create(self, db: AsyncSession, obj_in: UserCreate):
        user = User(**obj_in.dict())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def get(self, db: AsyncSession, user_id: int):
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def update(self, db: AsyncSession, db_obj: User, obj_in: UserUpdate):
        for field, value in obj_in.dict(exclude_unset=True).items():
            setattr(db_obj, field, value)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, db_obj: User):
        await db.delete(db_obj)
        await db.commit()
        return db_obj

    async def get_multi(self, db: AsyncSession):
        result = await db.execute(select(User))
        return result.scalars().all()

user = CRUDUser()
