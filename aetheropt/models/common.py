from typing import Dict, Any, Optional, List
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str
