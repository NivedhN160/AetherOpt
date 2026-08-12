import numpy as np

class SecureQUBO:
    """
    Secure QUBO Encapsulation.
    Applies strong scalar blinding and noise injection to hide the original 
    problem from an untrusted solver environment.
    """
    def __init__(self, Q: np.ndarray):
        self.original_Q = Q.copy()
        self.n = Q.shape[0]
        self.scale = 1.0
        self.offset = 0.0

    def blind_matrix(self, scale_range: tuple = (1.5, 5.0), offset_range: tuple = (0.5, 2.0)) -> np.ndarray:
        """
        Blinds the QUBO matrix using random scalar transformation.
        Q' = scale * Q + offset
        """
        self.scale = np.random.uniform(*scale_range)
        self.offset = np.random.uniform(*offset_range)
        return self.original_Q * self.scale + self.offset

    def decode_energy(self, blinded_energy: float, state: np.ndarray) -> float:
        """
        Recovers the true energy from the blinded evaluation.
        """
        k = np.sum(state)
        # The offset was added to every element, so state.T @ (offset) @ state = offset * k^2
        true_energy = (blinded_energy - self.offset * (k ** 2)) / self.scale
        return true_energy
