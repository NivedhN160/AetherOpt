import numpy as np

def extract_qubo_features(Q: np.ndarray) -> dict:
    """
    Extracts structural features from a QUBO matrix to estimate difficulty.
    """
    n = Q.shape[0]
    
    # Sparsity
    non_zeros = np.count_nonzero(Q)
    density = non_zeros / (n * n)
    
    # Diagonal dominance
    diag = np.diag(Q)
    off_diag = Q - np.diag(diag)
    diag_mean = float(np.mean(np.abs(diag)))
    off_diag_mean = float(np.mean(np.abs(off_diag)))
    
    # Scale
    max_weight = float(np.max(np.abs(Q)))
    min_weight = float(np.min(np.abs(Q[Q != 0])) if non_zeros > 0 else 0)
    
    return {
        "size": n,
        "density": float(density),
        "diagonal_mean_abs": diag_mean,
        "off_diagonal_mean_abs": off_diag_mean,
        "max_weight": max_weight,
        "min_weight": min_weight,
        "dynamic_range": float(max_weight / min_weight) if min_weight > 0 else 0.0
    }
