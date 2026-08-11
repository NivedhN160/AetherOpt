import numpy as np
from aetheropt.solvers.classical.highs_solver import HighsSolver

def test_highs_solver_runs():
    Q = np.array([
        [-1, 2],
        [0, -1]
    ])
    solver = HighsSolver()
    result = solver.solve(Q, config={})
    
    assert result.solver_name == "highs"
    assert len(result.best_solution) == 2
    assert "status" in result.solver_metadata
