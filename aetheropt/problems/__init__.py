from aetheropt.problems.base import BaseProblem
from aetheropt.problems.portfolio import PortfolioProblem
from aetheropt.problems.qubo import GenericQUBOProblem
from aetheropt.problems.maxcut import MaxCutProblem

# Add routing and scheduling as they get fleshed out

def get_problem(problem_type: str, data: dict) -> BaseProblem:
    if problem_type == "portfolio":
        return PortfolioProblem(data)
    elif problem_type == "qubo":
        return GenericQUBOProblem(data)
    elif problem_type == "maxcut":
        return MaxCutProblem(data)
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")
