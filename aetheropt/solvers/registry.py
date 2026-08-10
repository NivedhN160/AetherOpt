from typing import Dict, Type
from aetheropt.solvers.base import BaseSolver

_SOLVER_REGISTRY: Dict[str, Type[BaseSolver]] = {}

def register_solver(name: str):
    def decorator(cls: Type[BaseSolver]):
        _SOLVER_REGISTRY[name] = cls
        return cls
    return decorator

def get_solver(name: str) -> BaseSolver:
    if name not in _SOLVER_REGISTRY:
        raise ValueError(f"Solver '{name}' not found")
    return _SOLVER_REGISTRY[name]()
