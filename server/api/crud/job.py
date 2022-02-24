from typing import List
from api.models import Job
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession

class JobCrud:
    @classmethod
    async def get_all_jobs(
        cls,
        db: AsyncSession,
    ) -> List[Job]: 
        return (
            await db.execute(select(Job).order_by(Job.title.desc())
            )
        )