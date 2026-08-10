from fastapi import APIRouter
from aetheropt.api.v1 import jobs, results
from aetheropt.api import health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(jobs.router, prefix="/v1/jobs", tags=["jobs"])
api_router.include_router(results.router, prefix="/v1/results", tags=["results"])
