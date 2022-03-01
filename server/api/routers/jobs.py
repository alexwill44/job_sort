from configparser import DuplicateOptionError
from datetime import datetime
from distutils.log import error
from sqlite3 import IntegrityError
from typing import List
from sqlalchemy import select 
import asyncio
from api.schemas.jobs import JobResponse, JobCreate
from fastapi import APIRouter, HTTPException, status, Depends
from api import schemas
from api.crud import JobCrud
from api.dependencies.db import get_db
from api.models import Job
from sqlalchemy.ext.asyncio import AsyncSession 


router = APIRouter(prefix="/app", tags=["jobs"])

@router.get("/alljobs")
async def get_jobs(db: AsyncSession = Depends(get_db)
) -> List[Job]:
    start = datetime.now()
    jobs = await JobCrud.get_all_jobs(db)
    finish = datetime.now()
    return jobs, finish - start
   
@router.get("/ajob")
async def get_job_by_id(id: int, db: AsyncSession = Depends(get_db)
) -> Job:
    start = datetime.now()
    job = await JobCrud.get_by_id(db, id)
    finish = datetime.now()
    return job, finish - start

@router.post("/addjob")
async def add_new_job(data:JobCreate, db: AsyncSession = Depends(get_db), ) -> Job:
    new_job = await JobCrud.add_job(db, data)
    try:
        await db.commit()
        return new_job
    except IntegrityError as err:
        await db.rollback()
        return err
