import numpy as np
import time
import json
import os
from prettytable import PrettyTable

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aetheropt.solvers.registry import get_solver
from aetheropt.config import settings

def generate_random_qubo(n: int, density: float = 0.5) -> np.ndarray:
    """Generate a random symmetric QUBO matrix."""
    Q = np.random.uniform(-1, 1, (n, n))
    mask = np.random.rand(n, n) > density
    Q[mask] = 0
    # Make symmetric
    Q = (Q + Q.T) / 2
    return Q

def run_benchmark():
    sizes = [10, 50, 100]
    solvers = [
        "classical_sa",
        "quantum_inspired_sa",
        "simulated_bifurcation",
        "quantum_warmstart",
        "correlation_reduction"
    ]
    
    # We skip qaoa_local for huge sizes because it's simulated and will blow up RAM
    
    print("========================================")
    print(" AetherOpt Research Benchmarking Suite")
    print("========================================\n")
    
    for size in sizes:
        print(f"--- Benchmarking Problem Size: N={size} ---")
        Q = generate_random_qubo(size, density=0.7)
        
        table = PrettyTable()
        table.field_names = ["Solver", "Energy (Lower is better)", "Runtime (s)", "Status"]
        
        for solver_name in solvers:
            if solver_name == "qaoa_local" and size > settings.max_qaoa_qubits:
                continue
                
            try:
                solver = get_solver(solver_name)
                # Quick config for benchmarks
                config = {
                    "num_reads": 5, 
                    "num_steps": 500, 
                    "quantum_solver": "simulated_bifurcation",
                    "classical_solver": "classical_sa",
                    "correlation_threshold": 0.5
                }
                
                result = solver.solve(Q, config)
                table.add_row([
                    solver_name, 
                    f"{result.objective_value:.4f}", 
                    f"{result.runtime_seconds:.4f}",
                    "Success"
                ])
            except Exception as e:
                table.add_row([solver_name, "N/A", "N/A", f"Failed: {str(e)[:20]}"])
                
        print(table)
        print("\n")

if __name__ == "__main__":
    run_benchmark()
