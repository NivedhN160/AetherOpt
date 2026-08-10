from typing import List, Dict, Any
from aetheropt.models.result import ResultResponse

def compare_solvers(results: List[ResultResponse]) -> Dict[str, Any]:
    """
    Given a list of results from different solvers on the same problem,
    compute comparison metrics (e.g. best objective, fastest runtime).
    """
    if not results:
        return {}
        
    best_objective = min(r.objective_value for r in results)
    best_objective_solver = [r.solver_name for r in results if r.objective_value == best_objective]
    
    fastest_runtime = min(r.runtime_seconds for r in results)
    fastest_solver = [r.solver_name for r in results if r.runtime_seconds == fastest_runtime]
    
    return {
        "best_objective": best_objective,
        "best_objective_solver": best_objective_solver,
        "fastest_runtime": fastest_runtime,
        "fastest_solver": fastest_solver,
    }
