import numpy as np
from aetheropt.solvers.quantum_inspired_sa import QuantumInspiredSA

def test_quantum_inspired_sa_solve():
    Q = np.array([
        [-1, 2],
        [0, -1]
    ])
    solver = QuantumInspiredSA()
    result = solver.solve(Q, config={"num_reads": 5, "num_steps": 50, "seed": 42})
    
    assert result.solver_name == "quantum_inspired_sa"
    assert len(result.best_solution) == 2
    assert "energies" in result.solver_metadata
    assert len(result.solver_metadata["energies"]) > 0
