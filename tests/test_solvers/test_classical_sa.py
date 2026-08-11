import numpy as np
from aetheropt.solvers.classical.classical_sa import ClassicalSA

def test_classical_sa_solve():
    Q = np.array([
        [-1, 2],
        [0, -1]
    ])
    solver = ClassicalSA()
    result = solver.solve(Q, config={"num_reads": 2, "num_steps": 10})
    
    assert result.solver_name == "classical_sa"
    assert len(result.best_solution) == 2
    assert "energies" in result.solver_metadata
