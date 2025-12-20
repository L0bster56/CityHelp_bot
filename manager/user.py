from sqlalchemy import insert, inspect, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import User


class UserManager:
    def __init__(self, db:AsyncSession):
        self.db = db


    async def create(self, user_id:int,full_name:str):
        stmt = insert(User).values(
            id=user_id,
            full_name=full_name,
        ).returning(User)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def get(self, user_id:int):
        stmt = select(User).where(User.id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def list(self):
        stmt = select(User)
        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def update_language(self, user_id:int, language:str):
        stmt = update(User).where(User.id == user_id).values(language=language)
        await self.db.execute(stmt)
        await self.db.commit()

    async def update_role(self, user_id: int, role: str):
        stmt = update(User).where(User.id == user_id).values(role=role)
        await self.db.execute(stmt)
        await self.db.commit()

    async def update_phone(self, user_id: int, phone: str):
        stmt = update(User).where(User.id == user_id).values(phone=phone)
        await self.db.execute(stmt)
        await self.db.commit()

    async def delete(self, user_id:int):
        stmt = delete(User).where(User.id == user_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def get_or_create(self, user_id:int,full_name:str):
        user = await self.get(user_id)
        if user is None:
            user = await self.create(user_id,full_name)
        return user

