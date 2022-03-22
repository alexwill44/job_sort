import aiofiles
import csv

from datetime import datetime
from distutils.log import error
from sqlite3 import IntegrityError
from typing import List
from api.schemas.jobs import GetJobResponse, MultiJobsResponse, GetJobResponse, CreateJobResponse, JobCreate, ImportJobResponse
from fastapi import APIRouter, HTTPException, status, Depends, File, UploadFile
from api import schemas
from api.crud import JobCrud
from api.dependencies.db import get_db
from api.models import Job
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/app", tags=["jobs"])

@router.get("/alljobs", response_model=MultiJobsResponse)
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
    return ({"job":job, "message":f"{finish - start}"})

@router.post("/addjob", response_model=CreateJobResponse)
async def add_new_job(data:JobCreate, db: AsyncSession = Depends(get_db)) -> Job:
    new_job = await JobCrud.add_job(db, data)
    try:
        return({"job":new_job,"message":"posting added to db"})
    except IntegrityError as err:
        await db.rollback()
        return err

@router.post('/import', response_model=ImportJobResponse)
async def import_jobs(
    file: UploadFile = File(...),
    data: schemas.CSVupload = Depends(schemas.CSVupload.form_data),
    db: AsyncSession = Depends(get_db)
):
    file_content= await file.read()
    file_ref = f'{file.filename}_{datetime.now()}'
    async with aiofiles.open(file_ref, "wb") as upload:
        await upload.write(file_content)
    csv_reader = csv.reader(open(file_ref), delimiter="*")
    skip_header = data.skip_header
    overwrite = data.overwrite
    if skip_header: next(csv_reader)

    for row in csv_reader:
        if len(row) <= 0: continue

        posting = {
                "date_found" : row[0],
                "company" : row[1],
                "title" : row[2],
                "location" : row[3],
                "remote" : row[4],
                "link" : row[5],
            }

        job = await JobCrud.get_by_link(db, posting["link"]) 
        print (job)
        if job and overwrite:
            await JobCrud.update_job(
                job,
                posting['date_found'],
                posting["company"],
                posting["title"],
                posting["location"],
                posting["remote"],
                posting["link"],
                db,
            )    
            continue

        if job:
            continue

        else:
            await JobCrud.add_job(db, dict(posting))

    return {"message" : "ok!"}