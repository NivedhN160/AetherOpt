import hashlib
import json

def generate_hash_commitment(data: dict, nonce: str) -> str:
    """
    Generates a SHA-256 hash commitment of the problem data and a random nonce.
    """
    # Sort keys to ensure deterministic serialization
    payload = json.dumps(data, sort_keys=True)
    message = f"{nonce}|{payload}"
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

def verify_hash_commitment(data: dict, nonce: str, commitment: str) -> bool:
    """
    Verifies that the given data and nonce produce the given hash commitment.
    """
    expected_hash = generate_hash_commitment(data, nonce)
    return expected_hash == commitment
