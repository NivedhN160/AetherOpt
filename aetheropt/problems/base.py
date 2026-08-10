from abc import ABC, abstractmethod
import numpy as np
from typing import Tuple, Dict, Any

class BaseProblem(ABC):
    @abstractmethod
    def to_qubo(self) -> np.ndarray:
        """Returns the QUBO matrix Q"""
        pass
        
    @abstractmethod
    def interpret_solution(self, bitstring: np.ndarray) -> Any:
        """Translates a bitstring back into the problem's domain language"""
        pass
