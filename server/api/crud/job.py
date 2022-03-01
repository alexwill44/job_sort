from typing import List
from api.models import Job
from distutils.log import error
from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.jobs import JobCreate

class JobCrud:
    
    CACHE = {}
    
    @classmethod
    async def get_by_id(
        cls,
        db: AsyncSession,
        id: int
    ) -> Job : 
        global CACHE
        try: 
            async with db as session:
                result = await session.execute(select(Job).where(Job.id == id))
                CACHE = {i.id: i.title for i in result.scalars()}
                return CACHE
        except: 
            print(error)

    @classmethod
    async def get_all_jobs(
        cls,
        db: AsyncSession,
    ) -> List[Job]: 
        global CACHE
        try: 
            async with db as session:
                result = await session.execute(select(Job))
                CACHE = {i.id: i.title for i in result.scalars()}
                return CACHE
        except: 
            print(error)

    @classmethod
    async def add_job(
        cls, 
        db: AsyncSession,
        data: JobCreate
    ) -> Job:
        """ create a job posting """       
        job = Job(**dict(data))
        db.add(job)
        return job