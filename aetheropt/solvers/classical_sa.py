import numpy as np
import time
from typing import Dict, Any
from aetheropt.solvers.base import BaseSolver
from aetheropt.solvers.registry import register_solver
from aetheropt.models.result import SolverResultData

@register_solver("classical_sa")
class ClassicalSA(BaseSolver):
    def solve(self, Q: np.ndarray, config: Dict[str, Any]) -> SolverResultData:
        start_time = time.time()
        
        num_reads = config.get("num_reads", 10)
        num_steps = config.get("num_steps", 1000)
        initial_temp = config.get("initial_temp", 10.0)
        final_temp = config.get("final_temp", 0.01)
        
        n = Q.shape[0]
        best_overall_state = None
        best_overall_energy = float('inf')
        
        all_energies = []
        
        for read in range(num_reads):
            state = np.random.randint(2, size=n)
            energy = state.T @ Q @ state
            
            temp = initial_temp
            cooling_rate = (final_temp / initial_temp) ** (1 / num_steps)
            
            for step in range(num_steps):
                # Flip a random bit
                idx = np.random.randint(n)
                # Change in energy if we flip state[idx]
                # delta_E = Q[idx, idx]*(1 - 2*state[idx]) + sum_{j != idx} 2 * Q[idx, j] * state[j] * (1 - 2*state[idx])
                # A simpler way is just to evaluate full energy:
                new_state = state.copy()
                new_state[idx] = 1 - new_state[idx]
                
                new_energy = new_state.T @ Q @ new_state
                delta_E = new_energy - energy
                
                if delta_E < 0 or np.random.rand() < np.exp(-delta_E / temp):
                    state = new_state
                    energy = new_energy
                    
                temp *= cooling_rate
                
            all_energies.append(energy)
            if energy < best_overall_energy:
                best_overall_energy = energy
                best_overall_state = state
                
        runtime = time.time() - start_time
        return SolverResultData(
            solver_name="classical_sa",
            best_solution=best_overall_state.tolist(),
            objective_value=float(best_overall_energy),
            runtime_seconds=runtime,
            solver_metadata={"energies": [float(e) for e in all_energies]}
        )
