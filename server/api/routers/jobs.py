from datetime import datetime
from distutils.log import error
from sqlite3 import IntegrityError
from typing import List
from api.schemas.jobs import GetJobResponse, AllJobsResponse, GetJobResponse, CreateJobResponse, JobCreate
from fastapi import APIRouter, HTTPException, status, Depends
from api import schemas
from api.crud import JobCrud
from api.dependencies.db import get_db
from api.models import Job
from sqlalchemy.ext.asyncio import AsyncSession 


router = APIRouter(prefix="/app", tags=["jobs"])

@router.get("/alljobs", response_model=AllJobsResponse)
async def get_jobs(db: AsyncSession = Depends(get_db)
) -> List[Job]:
    start = datetime.now()
    jobs = await JobCrud.get_all_jobs(db)
    finish = datetime.now()
    return ({"jobs":jobs, "runtime":f"{finish - start}"})
   
@router.get("/ajob", response_model=GetJobResponse)
async def get_job_by_id(id: int, db: AsyncSession = Depends(get_db)
) -> Job:
    start = datetime.now()
    job = await JobCrud.get_by_id(db, id)
    finish = datetime.now()
    return ({"job":job, "runtime":f"{finish - start}"})

@router.post("/addjob", response_model=CreateJobResponse)
async def add_new_job(data:JobCreate, db: AsyncSession = Depends(get_db)) -> Job:
    new_job = await JobCrud.add_job(db, data)
    try:
        await db.commit()
        return({"job":new_job,"message":"posting added to db"})
    except IntegrityError as err:
        await db.rollback()
        return err
