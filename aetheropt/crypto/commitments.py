import secrets
import numpy as np
from typing import Dict, Tuple
from aetheropt.crypto.hash_primitives import generate_hash_commitment

class ProblemCommitment:
    """
    Manages the cryptographic commitment lifecycle for a QUBO problem.
    """
    def __init__(self, problem_data: dict):
        self.problem_data = problem_data
        self.nonce = secrets.token_hex(16)
        self.commitment = generate_hash_commitment(problem_data, self.nonce)
        
    def get_commitment_payload(self) -> Dict[str, str]:
        """
        Returns the commitment to be stored or sent to the client.
        """
        return {
            "commitment": self.commitment,
            "nonce": self.nonce
        }
