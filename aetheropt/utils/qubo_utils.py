import numpy as np

def qubo_to_ising(Q: np.ndarray):
    """
    Convert QUBO matrix Q to Ising J (couplings) and h (linear biases).
    x = (z + 1) / 2
    """
    n = Q.shape[0]
    J = np.zeros((n, n))
    h = np.zeros(n)
    offset = 0.0

    for i in range(n):
        for j in range(n):
            if i == j:
                h[i] += Q[i, i] / 2
                offset += Q[i, i] / 2
            else:
                J[i, j] += Q[i, j] / 4
                h[i] += Q[i, j] / 4
                h[j] += Q[i, j] / 4
                offset += Q[i, j] / 4
                
    return h, J, offset
