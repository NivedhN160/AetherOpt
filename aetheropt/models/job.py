from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class JobResponse(BaseModel):
    id: str
    problem_type: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
