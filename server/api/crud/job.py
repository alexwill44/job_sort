from typing import List
from api.models import Job
from distutils.log import error
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.schemas.jobs import JobCreate

class JobCrud:
    
    
    
    @classmethod
    async def get_by_id(
        cls,
        db: AsyncSession,
        id: int
    ) -> Job : 
        CACHE = {}
        try: 
            async with db as session:
                result = await session.execute(select(Job).where(Job.id == id))
                CACHE = {i.id: i for i in result.scalars()}
                return CACHE[id]
        except: 
            print(error)

    @classmethod
    async def get_by_link(
        cls,
        db: AsyncSession,
        link: str
    ) -> Job: 
        CACHE = {}
        try: 
            async with db as session:
                result = await session.execute(select(Job).where(Job.link == link))
                CACHE = {i.id: i for i in result.scalars()}
                return CACHE
        except: 
            print(error)

    @classmethod
    async def get_all_jobs(
        cls,
        db: AsyncSession,
    ) -> List[Job]: 
        CACHE = {}
        try: 
            async with db as session:
                result = await session.execute(select(Job))
                CACHE = {i for i in result.scalars()}
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
        await db.commit()
        return job

    @classmethod
    async def update_job(
        cls, 
        job: Job,
        date_found: str,
        company: str,
        title: str,
        location: str,
        remote: str,
        link: str,
        db: AsyncSession
    ):
        """ update a job posting """

        job.date_found = date_found
        job.company = company
        job.title = title
        job.location = location
        job.remote = remote
        job.link = link
        await db.commit()
        db.refresh(job)
        return job

    
    
    
    
    @classmethod
    async def test(
        cls,
        db: AsyncSession,
        link: str
    ) -> Job: 
        CACHE = {}
        try: 
            async with db as session:
                result = await session.execute(select(Job).filter_by(Job.link == link).first())
                CACHE = {i.id: i for i in result.scalars()}
                return CACHE
        except: 
            print(error)