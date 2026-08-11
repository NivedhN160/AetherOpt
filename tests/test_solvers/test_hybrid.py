import numpy as np
from aetheropt.solvers.hybrid.quantum_classical_pipeline import QuantumWarmstartSolver

def test_quantum_warmstart_runs():
    Q = np.array([
        [-1,  2, -1],
        [ 2, -2,  1],
        [-1,  1, -1]
    ])
    solver = QuantumWarmstartSolver()
    
    # Run with default sub-solvers: simulated_bifurcation -> classical_sa
    config = {
        "quantum_solver": "simulated_bifurcation",
        "classical_solver": "classical_sa",
        "num_steps": 10  # short run for testing
    }
    
    result = solver.solve(Q, config)
    assert result.solver_name == "quantum_warmstart"
    assert len(result.best_solution) == 3
    assert "quantum_energy" in result.solver_metadata
