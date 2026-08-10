import numpy as np

def calculate_portfolio_metrics(expected_returns, covariance, weights):
    """Calculate portfolio return and risk based on selected weights (or bitstring)"""
    expected_returns = np.array(expected_returns)
    covariance = np.array(covariance)
    weights = np.array(weights)
    
    # Normalize weights to sum to 1 for basic financial metrics
    if weights.sum() > 0:
        normalized_weights = weights / weights.sum()
    else:
        normalized_weights = weights
        
    port_return = np.dot(normalized_weights, expected_returns)
    port_risk = np.sqrt(np.dot(normalized_weights.T, np.dot(covariance, normalized_weights)))
    
    return {
        "expected_return": float(port_return),
        "risk_std_dev": float(port_risk)
    }
