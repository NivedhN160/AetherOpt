import numpy as np
from typing import Dict, Any
from aetheropt.problems.base import BaseProblem

class SchedulingProblem(BaseProblem):
    def __init__(self, data: Dict[str, Any]):
        self.num_tasks = data["num_tasks"]
        self.num_machines = data["num_machines"]
        self.task_lengths = data["task_lengths"]

    def to_qubo(self) -> np.ndarray:
        # Partition tasks into machines to minimize makespan (or sum of squares of loads)
        # We'll use sum of squares of loads for simplicity
        # let x_i,m = 1 if task i on machine m
        N = self.num_tasks
        M = self.num_machines
        Q = np.zeros((N*M, N*M))
        penalty = 1000.0 * max(self.task_lengths)**2
        
        # Constraint: each task on exactly one machine
        for i in range(N):
            for m1 in range(M):
                idx1 = i * M + m1
                Q[idx1, idx1] -= penalty
                for m2 in range(m1 + 1, M):
                    idx2 = i * M + m2
                    Q[idx1, idx2] += 2 * penalty
                    
        # Objective: minimize sum_m (sum_i x_i,m L_i)^2
        # = sum_m sum_i sum_j x_i,m x_j,m L_i L_j
        for m in range(M):
            for i in range(N):
                idx1 = i * M + m
                Q[idx1, idx1] += self.task_lengths[i]**2
                for j in range(i + 1, N):
                    idx2 = j * M + m
                    Q[idx1, idx2] += 2 * self.task_lengths[i] * self.task_lengths[j]
                    
        return Q

    def interpret_solution(self, bitstring: np.ndarray) -> Dict[str, Any]:
        N = self.num_tasks
        M = self.num_machines
        schedule = {m: [] for m in range(M)}
        
        for i in range(N):
            for m in range(M):
                idx = i * M + m
                if bitstring[idx] == 1:
                    schedule[m].append(i)
                    
        return {"schedule": schedule}
