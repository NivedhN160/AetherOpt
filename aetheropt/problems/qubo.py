import numpy as np
from typing import Dict, Any
from aetheropt.problems.base import BaseProblem

class GenericQUBOProblem(BaseProblem):
    def __init__(self, data: Dict[str, Any]):
        self.Q = np.array(data["Q"])
        
    def to_qubo(self) -> np.ndarray:
        return self.Q
        
    def interpret_solution(self, bitstring: np.ndarray) -> Dict[str, Any]:
        return {"bitstring": bitstring.tolist()}
