from datetime import datetime

from sqlalchemy import insert,  select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.reports import Report

class ReportManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        request_id: int,
        text: str,
        address: str,
        status: str,
        created_at: datetime
    ):
        stmt = insert(Report).values(
            request_id=request_id,
            text=text,
            address=address,
            status=status,
            created_at=created_at,
            date_end=datetime.now()
        ).returning(Report)

        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()

