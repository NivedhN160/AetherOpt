import hashlib
import json
from typing import Any, Dict

def compute_qubo_hash(Q: Any) -> str:
    """
    Compute a SHA-256 hash of a QUBO matrix or dictionary to ensure integrity
    before passing it to external solver nodes or storing it.
    """
    if hasattr(Q, "tolist"):
        data = Q.tolist()
    else:
        data = Q
        
    encoded = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

def verify_integrity(Q: Any, expected_hash: str) -> bool:
    """
    Verify the QUBO matrix against a known hash.
    """
    return compute_qubo_hash(Q) == expected_hash
