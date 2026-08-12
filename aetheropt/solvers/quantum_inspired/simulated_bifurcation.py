import numpy as np
import time
from typing import Dict, Any
from aetheropt.solvers.base import BaseSolver
from aetheropt.solvers.registry import register_solver
from aetheropt.models.result import SolverResultData

@register_solver("simulated_bifurcation")
class SimulatedBifurcationSolver(BaseSolver):
    """
    Simulated Bifurcation (SB) algorithm for solving QUBO problems.
    This is a highly scalable quantum-inspired algorithm based on simulating 
    nonlinear Hamiltonian dynamics of Kerr-nonlinear parametric oscillators.
    """
    def solve(self, Q: np.ndarray, config: Dict[str, Any]) -> SolverResultData:
        start_time = time.time()
        n = Q.shape[0]
        
        steps = config.get("num_steps", 1000)
        num_reads = config.get("num_reads", 10)
        dt = config.get("dt", 0.05)
        a0 = config.get("a0", 1.0)
        c0 = config.get("c0", 0.5)

        Q_sym = 0.5 * (Q + Q.T)
        
        # Convert QUBO to Ising
        J = -0.25 * Q_sym
        np.fill_diagonal(J, 0)
        h = -0.5 * np.diag(Q_sym) - 0.25 * (np.sum(Q_sym, axis=1) - np.diag(Q_sym))

        best_energy = float("inf")
        best_state = None
        energies = []

        for _ in range(num_reads):
            x = np.random.uniform(-0.1, 0.1, n)
            y = np.random.uniform(-0.1, 0.1, n)

            for t in range(steps):
                p = a0 * (t / steps)          # pump schedule
                
                # Symplectic Euler
                y = y + dt * (-(x**3) + p * x + (J @ x) + h)
                x = x + dt * c0 * y

            spins = np.sign(x)
            spins[spins == 0] = 1
            state = ((spins + 1) / 2).astype(int)

            energy = float(state @ Q_sym @ state)
            energies.append(energy)

            if energy < best_energy:
                best_energy = energy
                best_state = state.copy()

        return SolverResultData(
            solver_name="simulated_bifurcation",
            best_solution=best_state.tolist() if best_state is not None else [],
            objective_value=best_energy,
            runtime_seconds=time.time() - start_time,
            solver_metadata={
                "status": "completed",
                "num_reads": num_reads,
                "steps": steps,
                "best_energy": best_energy,
                "mean_energy": float(np.mean(energies)) if energies else 0.0
            }
        )
