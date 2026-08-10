from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ProblemData(BaseModel):
    # Depending on problem type, this can have different structures.
    # For simplicity, we accept a flexible dict and validate downstream if needed
    data: Dict[str, Any]

class ProblemRequest(BaseModel):
    problem_type: str = Field(..., description="E.g., 'portfolio', 'scheduling', 'routing', 'maxcut', 'qubo'")
    data: Dict[str, Any]
    solvers: List[str] = Field(..., description="List of solvers to run, e.g. ['quantum_inspired_sa']")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)
