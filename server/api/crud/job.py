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
        data: JobCreate,
        db: AsyncSession
    ):
        """ update a job posting """
        print(data)
        job.date_found = data.date_found
        job.company = data.company
        job.title = data.title
        job.location = data.location
        job.remote = data.remote
        job.link = data.link
        job.import_file_id = data.import_file_id
        await db.commit()
        db.refresh(job)
        return job

    @classmethod
    async def search_title(
        cls, 
        query: str,
        db:AsyncSession
    ):
        """search by whole or partial title"""
        CACHE = {}
        try: 
            async with db as session:
                jobs = await session.execute(select(Job).where(Job.title.contains(query)))
                CACHE = {i.id: i for i in jobs.scalars()}
                return CACHE
        except:
            print(error)
        
        return 