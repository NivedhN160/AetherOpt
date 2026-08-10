import numpy as np
from typing import Dict, Any
from aetheropt.problems.base import BaseProblem

class MaxCutProblem(BaseProblem):
    def __init__(self, data: Dict[str, Any]):
        self.W = np.array(data["adjacency_matrix"])
        self.n = self.W.shape[0]

    def to_qubo(self) -> np.ndarray:
        # MaxCut QUBO: minimize sum_{i<j} w_{ij} (2x_i x_j - x_i - x_j)
        Q = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    Q[i, i] -= self.W[i, j]
                    Q[i, j] += 2 * self.W[i, j]
        return Q

    def interpret_solution(self, bitstring: np.ndarray) -> Dict[str, Any]:
        set_s = [i for i, b in enumerate(bitstring) if b == 1]
        set_t = [i for i, b in enumerate(bitstring) if b == 0]
        
        cut_value = 0
        for i in set_s:
            for j in set_t:
                cut_value += self.W[i, j]
                
        return {
            "set_1": set_s,
            "set_2": set_t,
            "cut_value": cut_value
        }
