from typing import Dict, Any, List, Optional, Union, Literal
from pydantic import BaseModel, Field
from typing_extensions import Annotated

from pydantic import BaseModel, Field, model_validator

class PortfolioProblemData(BaseModel):
    expected_returns: List[float]
    covariance_matrix: List[List[float]]
    k: int = Field(ge=1)
    risk_aversion: float = Field(default=0.5)

    @model_validator(mode='after')
    def check_shapes(self) -> 'PortfolioProblemData':
        n = len(self.expected_returns)
        if len(self.covariance_matrix) != n:
            raise ValueError(f"covariance_matrix must have {n} rows")
        for row in self.covariance_matrix:
            if len(row) != n:
                raise ValueError(f"covariance_matrix must be square ({n}x{n})")
        if self.k > n:
            raise ValueError(f"k cannot be greater than number of assets ({n})")
        return self

class MaxCutProblemData(BaseModel):
    adjacency_matrix: List[List[float]]

    @model_validator(mode='after')
    def check_shapes(self) -> 'MaxCutProblemData':
        n = len(self.adjacency_matrix)
        for row in self.adjacency_matrix:
            if len(row) != n:
                raise ValueError("adjacency_matrix must be square")
        return self

class SchedulingProblemData(BaseModel):
    num_tasks: int = Field(ge=1)
    num_machines: int = Field(ge=1)
    task_lengths: List[float]

    @model_validator(mode='after')
    def check_shapes(self) -> 'SchedulingProblemData':
        if len(self.task_lengths) != self.num_tasks:
            raise ValueError(f"task_lengths must have {self.num_tasks} elements")
        return self

class RoutingProblemData(BaseModel):
    num_locations: int = Field(ge=2)
    distance_matrix: List[List[float]]
    num_vehicles: int = Field(ge=1)

    @model_validator(mode='after')
    def check_shapes(self) -> 'RoutingProblemData':
        n = self.num_locations
        if len(self.distance_matrix) != n:
            raise ValueError(f"distance_matrix must have {n} rows")
        for row in self.distance_matrix:
            if len(row) != n:
                raise ValueError(f"distance_matrix must be square ({n}x{n})")
        return self

class GenericQUBOData(BaseModel):
    Q: List[List[float]]
    higher_order_terms: Optional[List[Dict[str, Any]]] = Field(default=None, description="Support for PUBO (Polynomial Unconstrained Binary Optimization)")

    @model_validator(mode='after')
    def check_shapes(self) -> 'GenericQUBOData':
        n = len(self.Q)
        for row in self.Q:
            if len(row) != n:
                raise ValueError("Q matrix must be square")
        return self

class BaseProblemRequest(BaseModel):
    solvers: List[str] = Field(..., description="List of solvers to run, e.g. ['quantum_inspired_sa']")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict)
    multi_objective_weights: Optional[Dict[str, float]] = Field(default=None, description="Weights for multi-objective optimization (e.g. {'risk': 0.5, 'return': 0.5})")

class PortfolioRequest(BaseProblemRequest):
    problem_type: Literal["portfolio"]
    data: PortfolioProblemData

class MaxCutRequest(BaseProblemRequest):
    problem_type: Literal["maxcut"]
    data: MaxCutProblemData

class SchedulingRequest(BaseProblemRequest):
    problem_type: Literal["scheduling"]
    data: SchedulingProblemData

class RoutingRequest(BaseProblemRequest):
    problem_type: Literal["routing"]
    data: RoutingProblemData

class QUBORequest(BaseProblemRequest):
    problem_type: Literal["qubo"]
    data: GenericQUBOData

ProblemRequest = Annotated[
    Union[PortfolioRequest, MaxCutRequest, SchedulingRequest, RoutingRequest, QUBORequest],
    Field(discriminator="problem_type")
]
