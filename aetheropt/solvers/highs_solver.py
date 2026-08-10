import numpy as np
import time
import highspy
from typing import Dict, Any
from aetheropt.solvers.base import BaseSolver
from aetheropt.solvers.registry import register_solver
from aetheropt.models.result import SolverResultData

@register_solver("highs")
class HighsSolver(BaseSolver):
    def solve(self, Q: np.ndarray, config: Dict[str, Any]) -> SolverResultData:
        start_time = time.time()
        
        n = Q.shape[0]
        max_size = config.get("max_size", 100)
        if n > max_size:
            raise ValueError(f"Problem size n={n} is too large for local HiGHS solver (max {max_size}).")
            
        try:
            h = highspy.Highs()
            
            # Add variables x_i
            h.addVars(n, np.zeros(n), np.ones(n))
            for i in range(n):
                h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
                
            # Add variables for x_i * x_j (y_ij)
            num_pairs = (n * (n - 1)) // 2
            
            if num_pairs > 0:
                h.addVars(num_pairs, np.zeros(num_pairs), np.ones(num_pairs))
                
                pair_idx = 0
                for i in range(n):
                    for j in range(i + 1, n):
                        y_idx = n + pair_idx
                        
                        h.addRow(-highspy.kHighsInf, 0.0, 2, np.array([y_idx, i]), np.array([1.0, -1.0]))
                        h.addRow(-highspy.kHighsInf, 0.0, 2, np.array([y_idx, j]), np.array([1.0, -1.0]))
                        h.addRow(-1.0, highspy.kHighsInf, 3, np.array([y_idx, i, j]), np.array([1.0, -1.0, -1.0]))
                        
                        pair_idx += 1
            
            # Objective
            for i in range(n):
                h.changeColCost(i, Q[i, i])
                
            pair_idx = 0
            for i in range(n):
                for j in range(i + 1, n):
                    y_idx = n + pair_idx
                    h.changeColCost(y_idx, Q[i, j] + Q[j, i])
                    pair_idx += 1
                    
            h.changeObjectiveSense(highspy.ObjSense.kMinimize)
            h.setOptionValue("output_flag", False)
            
            # Time limit
            time_limit = config.get("time_limit", 60.0)
            h.setOptionValue("time_limit", time_limit)
            
            h.run()
            
            info = h.getInfo()
            solution = h.getSolution()
            
            if not solution.col_value:
                raise RuntimeError("HiGHS returned no solution.")
                
            x_sol = solution.col_value[:n]
            best_state = np.round(x_sol).astype(int)
            
            runtime = time.time() - start_time
            
            return SolverResultData(
                solver_name="highs",
                best_solution=best_state.tolist(),
                objective_value=info.objective_function_value,
                runtime_seconds=runtime,
                solver_metadata={"status": h.getModelStatus().name}
            )
        except Exception as e:
            raise RuntimeError(f"HiGHS solver failed: {e}")
