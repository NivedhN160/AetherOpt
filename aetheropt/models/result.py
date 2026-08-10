from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class SolverResultData(BaseModel):
    solver_name: str
    best_solution: Any
    objective_value: float
    runtime_seconds: float
    solver_metadata: Dict[str, Any] = {}

class ResultResponse(BaseModel):
    id: int
    job_id: str
    solver_name: str
    best_solution: Any
    objective_value: float
    runtime_seconds: float
    solver_metadata: Dict[str, Any]
    
    class Config:
        from_attributes = True

class JobResultResponse(BaseModel):
    job_id: str
    status: str
    problem_type: str
    results: List[ResultResponse]
    error_message: Optional[str] = None
