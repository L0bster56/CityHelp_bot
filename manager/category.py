from sqlalchemy import insert,  select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.category import Category

class CategoryManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, category_id: int):
        stmt = select(Category).where(Category.id == category_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()


    async def list(self):
        stmt = select(Category)
        result = await self.db.execute(stmt)
        return result.scalars().all()