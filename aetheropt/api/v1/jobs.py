from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List

from aetheropt.db.session import get_db
from aetheropt.models.problem import ProblemRequest
from aetheropt.models.job import JobResponse
from aetheropt.services.job_service import create_job, run_job
from aetheropt.core.security import get_api_key

router = APIRouter()

@router.post("/", response_model=JobResponse)
def submit_job(
    request: ProblemRequest, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    job = create_job(db, request)
    background_tasks.add_task(run_job, job.id, db)
    return job

@router.get("/{job_id}", response_model=JobResponse)
def get_job_status(
    job_id: str, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    from aetheropt.db.models import Job
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
