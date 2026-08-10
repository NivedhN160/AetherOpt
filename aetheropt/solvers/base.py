from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Any
from aetheropt.models.result import SolverResultData

class BaseSolver(ABC):
    @abstractmethod
    def solve(self, Q: np.ndarray, config: Dict[str, Any]) -> SolverResultData:
        pass
