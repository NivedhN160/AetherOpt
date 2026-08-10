import numpy as np
from typing import Dict, Any, List
from aetheropt.problems.base import BaseProblem
from aetheropt.core.exceptions import ProblemFormulationError

class PortfolioProblem(BaseProblem):
    def __init__(self, data: Dict[str, Any]):
        try:
            self.mu = np.array(data["expected_returns"])
            self.cov = np.array(data["covariance_matrix"])
            self.risk_aversion = data.get("risk_aversion", 0.5)
            self.k = data.get("k", len(self.mu) // 2)
            self.penalty = data.get("penalty", 10.0)
            self.n = len(self.mu)
        except KeyError as e:
            raise ProblemFormulationError(f"Missing required portfolio data: {e}")

    def to_qubo(self) -> np.ndarray:
        # Objective: minimize -risk_aversion * mu^T x + (1-risk_aversion) x^T Cov x
        # Constraint: sum(x) = k  => penalty * (sum(x) - k)^2
        
        Q = np.zeros((self.n, self.n))
        
        for i in range(self.n):
            Q[i, i] = -self.risk_aversion * self.mu[i]
            for j in range(self.n):
                Q[i, j] += (1 - self.risk_aversion) * self.cov[i, j]
                
        # Add constraint (sum(x_i) - k)^2 = sum_i x_i^2 + 2 sum_{i<j} x_i x_j - 2k sum_i x_i + k^2
        for i in range(self.n):
            Q[i, i] += self.penalty * (1 - 2 * self.k)
            for j in range(self.n):
                if i != j:
                    Q[i, j] += self.penalty

        return Q
        
    def interpret_solution(self, bitstring: np.ndarray) -> Dict[str, Any]:
        selected = [i for i, bit in enumerate(bitstring) if bit == 1]
        return {
            "selected_assets": selected,
            "num_selected": len(selected)
        }
