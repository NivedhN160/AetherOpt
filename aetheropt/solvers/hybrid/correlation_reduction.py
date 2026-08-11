import numpy as np
import time
from typing import Dict, Any
from aetheropt.solvers.base import BaseSolver
from aetheropt.solvers.registry import register_solver, get_solver
from aetheropt.models.result import SolverResultData

import logging
logger = logging.getLogger(__name__)

@register_solver("correlation_reduction")
class CorrelationReductionSolver(BaseSolver):
    """
    Quantum-inspired correlation-based problem reduction.
    Finds strongly correlated variables (or massive linear biases) and freezes them,
    reducing the problem size before passing it to an exact or hybrid solver.
    """
    def solve(self, Q: np.ndarray, config: Dict[str, Any]) -> SolverResultData:
        start_time = time.time()
        n = Q.shape[0]
        
        # 1. Reduction Phase
        threshold = config.get("correlation_threshold", 0.5)
        
        # Heuristic: Find linear terms that are vastly larger than quadratic connections
        # OR find variables that are essentially disconnected.
        linear_terms = np.diag(Q)
        max_q = np.max(np.abs(Q))
        if max_q == 0: max_q = 1.0 # avoid div by zero
        
        frozen_vars = {}
        for i in range(n):
            # If linear cost is extremely high and positive, variable prefers to be 0
            # If extremely high and negative, prefers to be 1
            if linear_terms[i] > threshold * max_q:
                frozen_vars[i] = 0
            elif linear_terms[i] < -threshold * max_q:
                frozen_vars[i] = 1
                
        logger.info(f"Correlation Reduction: Froze {len(frozen_vars)} out of {n} variables.")
        
        # If we froze everything, we're done
        if len(frozen_vars) == n:
            best_state = np.zeros(n, dtype=int)
            for i, v in frozen_vars.items():
                best_state[i] = v
            energy = best_state.T @ Q @ best_state
            return SolverResultData(
                solver_name="correlation_reduction",
                best_solution=best_state.tolist(),
                objective_value=float(energy),
                runtime_seconds=time.time() - start_time,
                solver_metadata={"status": "completed_by_reduction", "frozen_count": n}
            )
            
        # 2. Build Reduced QUBO
        active_vars = [i for i in range(n) if i not in frozen_vars]
        new_n = len(active_vars)
        Q_reduced = np.zeros((new_n, new_n))
        
        # Map original index to new index
        idx_map = {old: new for new, old in enumerate(active_vars)}
        
        for i in active_vars:
            for j in active_vars:
                Q_reduced[idx_map[i], idx_map[j]] = Q[i, j]
                
        # Add linear biases from frozen variables interacting with active ones
        for i in active_vars:
            bias = 0
            for fj, fv in frozen_vars.items():
                if fv == 1:
                    bias += Q[i, fj] + Q[fj, i]
            Q_reduced[idx_map[i], idx_map[i]] += bias
            
        # Constant energy offset from frozen-frozen interactions
        frozen_energy = 0
        for fi, fvi in frozen_vars.items():
            if fvi == 1:
                frozen_energy += Q[fi, fi]
                for fj, fvj in frozen_vars.items():
                    if fvj == 1 and fi != fj:
                        frozen_energy += Q[fi, fj]
        
        # 3. Solve Reduced QUBO
        sub_solver_name = config.get("sub_solver", "quantum_warmstart")
        logger.info(f"Solving reduced problem of size {new_n} with {sub_solver_name}")
        
        try:
            sub_solver = get_solver(sub_solver_name)
            sub_result = sub_solver.solve(Q_reduced, config)
            reduced_state = sub_result.best_solution
        except Exception as e:
            logger.error(f"Sub-solver {sub_solver_name} failed: {e}")
            return SolverResultData(
                solver_name="correlation_reduction",
                best_solution=[],
                objective_value=float('inf'),
                runtime_seconds=time.time() - start_time,
                solver_metadata={"status": "failed", "error": f"Sub-solver failed: {e}"}
            )

        # 4. Reconstruct Full State
        full_state = np.zeros(n, dtype=int)
        for i, v in frozen_vars.items():
            full_state[i] = v
        for i, val in enumerate(reduced_state):
            full_state[active_vars[i]] = val
            
        final_energy = full_state.T @ Q @ full_state
        
        return SolverResultData(
            solver_name="correlation_reduction",
            best_solution=full_state.tolist(),
            objective_value=float(final_energy),
            runtime_seconds=time.time() - start_time,
            solver_metadata={
                "status": "completed",
                "frozen_count": len(frozen_vars),
                "sub_solver": sub_solver_name,
                "sub_solver_runtime": sub_result.runtime_seconds
            }
        )
