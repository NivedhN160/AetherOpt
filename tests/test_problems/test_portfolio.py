from aetheropt.problems.portfolio import PortfolioProblem
import numpy as np

def test_portfolio_problem_creation():
    data = {
        "expected_returns": [0.1, 0.2],
        "covariance_matrix": [[0.04, 0.01], [0.01, 0.05]],
        "k": 1,
        "risk_aversion": 0.5
    }
    problem = PortfolioProblem(data)
    Q = problem.to_qubo()
    
    assert Q.shape == (2, 2)
    # Check that matrix is not all zeros
    assert not np.all(Q == 0)
