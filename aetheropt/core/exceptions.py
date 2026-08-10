from fastapi import HTTPException

class AetherOptException(Exception):
    pass

class SolverError(AetherOptException):
    pass

class ProblemFormulationError(AetherOptException):
    pass
