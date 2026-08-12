import numpy as np
from aetheropt.crypto.hash_primitives import verify_hash_commitment

class ResultVerification:
    """
    Verifies that the returned solution from the solver matches the 
    cryptographically committed problem data.
    """
    @staticmethod
    def verify_solution(problem_data: dict, nonce: str, commitment: str, 
                        solution: list, q_matrix: np.ndarray, reported_energy: float) -> bool:
        """
        Verify that:
        1. The problem data hashes to the commitment.
        2. The solution state on the actual Q matrix matches the reported energy.
        """
        # 1. Verify commitment
        if not verify_hash_commitment(problem_data, nonce, commitment):
            return False
            
        # 2. Verify energy
        if solution:
            state = np.array(solution)
            actual_energy = float(state.T @ q_matrix @ state)
            # Allow small floating point tolerance
            if abs(actual_energy - reported_energy) > 1e-4:
                return False
                
        return True
