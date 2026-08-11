import numpy as np

class SecureQUBO:
    """
    Secure QUBO encapsulation.
    Provides methods to blind or encrypt QUBO coefficients (e.g., adding noise
    or using homomorphic-like scalar transformations) before sending to untrusted solvers,
    and reconstructing the true energy locally.
    """
    
    def __init__(self, Q: np.ndarray):
        self.original_Q = Q
        self.n = Q.shape[0]
        
    def blind_matrix(self, scale: float = 1.5, offset: float = 0.5) -> np.ndarray:
        """
        Applies a simple scalar blinding to the QUBO matrix.
        (Note: This is a placeholder for actual cryptographic blinding or Homomorphic Encryption).
        """
        # A simple linear transformation Q' = scale * Q + offset
        return self.original_Q * scale + offset
        
    def decode_energy(self, blinded_energy: float, state: np.ndarray, scale: float = 1.5, offset: float = 0.5) -> float:
        """
        Recover the true energy from the blinded evaluation.
        """
        # number of ones in state
        k = np.sum(state)
        # The offset was added to every element, so state.T @ (offset) @ state = offset * k^2
        # blinded_energy = scale * true_energy + offset * k^2
        true_energy = (blinded_energy - offset * (k ** 2)) / scale
        return true_energy
