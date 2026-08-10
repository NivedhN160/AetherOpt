from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from aetheropt.db.session import get_db
from aetheropt.models.result import JobResultResponse, ResultResponse
from aetheropt.core.security import get_api_key
from aetheropt.db.models import Job, Result

router = APIRouter()

@router.get("/{job_id}", response_model=JobResultResponse)
def get_job_results(
    job_id: str, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    return {
        "job_id": job.id,
        "status": job.status,
        "problem_type": job.problem_type,
        "error_message": job.error_message,
        "results": job.results
    }
