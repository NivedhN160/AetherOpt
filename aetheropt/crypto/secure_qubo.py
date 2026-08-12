import numpy as np

class SecureQUBO:
    """
    Secure QUBO Encapsulation.
    Applies strong scalar blinding and permutation obfuscation to hide the original 
    problem from an untrusted solver environment.
    """
    def __init__(self, Q: np.ndarray):
        self.original_Q = Q.copy()
        self.n = Q.shape[0]
        self.scale = 1.0
        self.offset = 0.0
        self.permutation = np.arange(self.n)
        self.inverse_permutation = np.arange(self.n)

    def blind_matrix(self, scale_range: tuple = (1.5, 5.0), offset_range: tuple = (0.5, 2.0)) -> np.ndarray:
        """
        Blinds the QUBO matrix using random scalar transformation and permutation.
        Q' = P^T (scale * Q + offset) P
        """
        self.scale = np.random.uniform(*scale_range)
        self.offset = np.random.uniform(*offset_range)
        
        # 1. Scale and Offset
        scaled_Q = self.original_Q * self.scale + self.offset
        
        # 2. Permutation
        self.permutation = np.random.permutation(self.n)
        self.inverse_permutation = np.argsort(self.permutation)
        
        # Apply permutation to rows and columns
        blinded_Q = scaled_Q[self.permutation, :][:, self.permutation]
        return blinded_Q

    def decode_solution(self, blinded_state: list) -> list:
        """
        Recovers the true solution vector from the blinded evaluation.
        """
        state_array = np.array(blinded_state)
        # Apply inverse permutation
        true_state = state_array[self.inverse_permutation]
        return true_state.tolist()

    def decode_energy(self, blinded_energy: float, state: list) -> float:
        """
        Recovers the true energy from the blinded evaluation.
        Note: The state passed here should be the ORIGINAL decoded state.
        """
        state_array = np.array(state)
        k = np.sum(state_array)
        # The offset was added to every element, so state.T @ (offset) @ state = offset * k^2
        true_energy = (blinded_energy - self.offset * (k ** 2)) / self.scale
        return true_energy
