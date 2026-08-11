import numpy as np
import time
from typing import Dict, Any
from aetheropt.solvers.base import BaseSolver
from aetheropt.solvers.registry import register_solver, get_solver
from aetheropt.models.result import SolverResultData

import logging
logger = logging.getLogger(__name__)

@register_solver("quantum_warmstart")
class QuantumWarmstartSolver(BaseSolver):
    """
    Hybrid Solver that uses a quantum or quantum-inspired algorithm to find a good
    initial basin, then feeds it to a classical solver to refine exactly to the nearest local minima.
    """
    def solve(self, Q: np.ndarray, config: Dict[str, Any]) -> SolverResultData:
        start_time = time.time()
        
        # 1. Quantum Phase
        q_solver_name = config.get("quantum_solver", "simulated_bifurcation")
        logger.info(f"Quantum Warmstart: Running initial phase with {q_solver_name}")
        
        try:
            q_solver = get_solver(q_solver_name)
            q_result = q_solver.solve(Q, config)
            warm_state = q_result.best_solution
            q_runtime = q_result.runtime_seconds
        except Exception as e:
            logger.error(f"Quantum phase failed: {e}")
            return SolverResultData(
                solver_name="quantum_warmstart",
                best_solution=[],
                objective_value=float('inf'),
                runtime_seconds=time.time() - start_time,
                solver_metadata={"status": "failed", "error": f"Quantum phase failed: {e}"}
            )
            
        if not warm_state:
            return SolverResultData(
                solver_name="quantum_warmstart",
                best_solution=[],
                objective_value=float('inf'),
                runtime_seconds=time.time() - start_time,
                solver_metadata={"status": "failed", "error": "Quantum phase returned empty state"}
            )

        # 2. Classical Refinement Phase
        c_solver_name = config.get("classical_solver", "classical_sa")
        logger.info(f"Quantum Warmstart: Refining phase with {c_solver_name}")
        
        # We need to tell the classical solver to start from the warm state.
        # Ensure the classical solver accepts 'initial_state' in config
        c_config = config.copy()
        c_config["initial_state"] = warm_state
        
        try:
            c_solver = get_solver(c_solver_name)
            c_result = c_solver.solve(Q, c_config)
            final_state = c_result.best_solution
            final_energy = c_result.objective_value
            c_runtime = c_result.runtime_seconds
        except Exception as e:
            logger.error(f"Classical phase failed: {e}")
            return SolverResultData(
                solver_name="quantum_warmstart",
                best_solution=warm_state,
                objective_value=q_result.objective_value,
                runtime_seconds=time.time() - start_time,
                solver_metadata={"status": "partial", "error": f"Classical phase failed: {e}", "quantum_energy": q_result.objective_value}
            )
            
        total_runtime = time.time() - start_time
        
        return SolverResultData(
            solver_name="quantum_warmstart",
            best_solution=final_state,
            objective_value=final_energy,
            runtime_seconds=total_runtime,
            solver_metadata={
                "status": "completed",
                "quantum_solver": q_solver_name,
                "classical_solver": c_solver_name,
                "quantum_energy": q_result.objective_value,
                "quantum_runtime": q_runtime,
                "classical_runtime": c_runtime,
                "refinement_improvement": q_result.objective_value - final_energy
            }
        )
