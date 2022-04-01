from typing import List
from api.models import Job
from distutils.log import error
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update as sqlalchemy_update
from api.schemas.jobs import JobCreate

class JobCrud:
    
    
    @classmethod
    async def get_by_id(
        cls,
        db: AsyncSession,
        id: int
    ) -> Job : 
        try: 
            query = select(Job).where(Job.id == id)
            results = await db.execute(query)
            (result,)=results.one()
            return result
        except: 
            print(error)
            return error
        
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
                for i in result.scalars():
                    CACHE[f"{i.id}"] = {
                        "date_found": i.date_found,
                        "title": i.title,
                        "company": i.company,
                        "location": i.location,
                        "remote": i.remote,
                        "link": i.link
                        }
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
        for id in job:
            query = (
                sqlalchemy_update(Job)
                .where(Job.id == int(id))
                .values(**data)
                .execution_options(synchronize_session="fetch")
            )
            await db.execute(query)
            await db.commit()
        return  

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