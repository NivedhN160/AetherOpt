import numpy as np
import time
from typing import Dict, Any
from aetheropt.solvers.base import BaseSolver
from aetheropt.solvers.registry import register_solver
from aetheropt.models.result import SolverResultData
from aetheropt.config import settings

import logging
logger = logging.getLogger(__name__)

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import Aer
    from scipy.optimize import minimize
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False


@register_solver("qaoa_local")
class QAOALocalSolver(BaseSolver):
    """
    QAOA (Quantum Approximate Optimization Algorithm) solver.
    Uses Qiskit Aer local simulation.
    """
    def solve(self, Q: np.ndarray, config: Dict[str, Any]) -> SolverResultData:
        start_time = time.time()
        n = Q.shape[0]
        
        if n > settings.max_qaoa_qubits:
            return SolverResultData(
                solver_name="qaoa_local",
                best_solution=[],
                objective_value=float('inf'),
                runtime_seconds=time.time() - start_time,
                solver_metadata={"status": "failed", "error": f"Problem size {n} exceeds max QAOA qubits ({settings.max_qaoa_qubits})"}
            )
            
        if not QISKIT_AVAILABLE:
            return SolverResultData(
                solver_name="qaoa_local",
                best_solution=[],
                objective_value=float('inf'),
                runtime_seconds=time.time() - start_time,
                solver_metadata={"status": "failed", "error": "Qiskit not available"}
            )

        p = config.get("p", 1) # QAOA depth
        shots = config.get("num_reads", 1000)
        
        # Convert QUBO to Ising
        # For QUBO min x^T Q x
        # x_i = (1 - z_i)/2
        Q_sym = (Q + Q.T) / 2
        
        # Build Ising Hamiltonian
        h = np.zeros(n)
        J = np.zeros((n, n))
        
        offset = 0.0
        for i in range(n):
            offset += Q_sym[i, i] / 2
            h[i] -= Q_sym[i, i] / 2
            for j in range(i+1, n):
                offset += Q_sym[i, j] / 4
                h[i] -= Q_sym[i, j] / 4
                h[j] -= Q_sym[i, j] / 4
                J[i, j] += Q_sym[i, j] / 4

        # QAOA objective function
        backend = Aer.get_backend(settings.quantum_backend)
        
        def create_qaoa_circ(theta):
            beta = theta[:p]
            gamma = theta[p:]
            
            qc = QuantumCircuit(n)
            # Initial state
            qc.h(range(n))
            
            for layer in range(p):
                # Problem unitary
                for i in range(n):
                    if h[i] != 0:
                        qc.rz(2 * gamma[layer] * h[i], i)
                for i in range(n):
                    for j in range(i+1, n):
                        if J[i, j] != 0:
                            qc.rzz(2 * gamma[layer] * J[i, j], i, j)
                            
                # Mixer unitary
                for i in range(n):
                    qc.rx(2 * beta[layer], i)
                    
            qc.measure_all()
            return qc

        def compute_expectation(counts):
            avg = 0
            sum_count = 0
            for bit_string, count in counts.items():
                x = np.array([int(b) for b in bit_string[::-1]])
                val = x.T @ Q_sym @ x
                avg += val * count
                sum_count += count
            return avg / sum_count if sum_count > 0 else 0

        def get_expectation(theta):
            qc = create_qaoa_circ(theta)
            qc_transpiled = transpile(qc, backend)
            job = backend.run(qc_transpiled, shots=shots)
            result = job.result()
            counts = result.get_counts()
            return compute_expectation(counts)
            
        # Optimize parameters
        initial_theta = np.random.rand(2 * p) * np.pi
        res = minimize(get_expectation, initial_theta, method='COBYLA', options={'maxiter': config.get("maxiter", 30)})
        
        # Get optimal circuit and run to get best bitstring
        qc = create_qaoa_circ(res.x)
        qc_transpiled = transpile(qc, backend)
        job = backend.run(qc_transpiled, shots=shots)
        counts = job.result().get_counts()
        
        # Find best string
        best_str = max(counts, key=counts.get)
        best_state = np.array([int(b) for b in best_str[::-1]])
        best_energy = best_state.T @ Q_sym @ best_state
        
        runtime = time.time() - start_time
        
        return SolverResultData(
            solver_name="qaoa_local",
            best_solution=best_state.tolist(),
            objective_value=float(best_energy),
            runtime_seconds=runtime,
            solver_metadata={
                "status": "completed", 
                "p": p, 
                "optimization_success": res.success,
                "iterations": res.nfev
            }
        )
