from sqlalchemy import insert,  select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.requests import Request

class RequestManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user_id:int,category_id:int,text:str,address:str):
        stmt = insert(Request).values(
            user_id=user_id,
            category_id=category_id,
            text=text,
            address=address,
        ).returning(Request)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

    async def get(self, request_id:int):
        stmt = select(Request).where(Request.id == request_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def list(self):
        stmt = select(Request)
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def update_category(self, request_id: int, category_id: int):
        stmt = update(Request).where(Request.id == request_id).values(category_id=category_id)
        await self.db.execute(stmt)
        await self.db.commit()

    async def update_status(self, request_id: int, status: str):
        stmt = update(Request).where(Request.id == request_id).values(status=status)
        await self.db.execute(stmt)
        await self.db.commit()




    async def delete(self, request_id:int):
        stmt = delete(Request).where(Request.id == request_id)
        await self.db.execute(stmt)
        await self.db.commit()

