import uuid
import datetime
from sqlalchemy.orm import Session
from aetheropt.db.models import Job, Result
from aetheropt.models.problem import ProblemRequest
from aetheropt.problems import get_problem
from aetheropt.solvers.registry import get_solver
from aetheropt.core.logging import logger
import traceback

def create_job(db: Session, request: ProblemRequest) -> Job:
    job_id = str(uuid.uuid4())
    job = Job(
        id=job_id,
        problem_type=request.problem_type,
        status="pending",
        config={"data": request.data, "solvers": request.solvers, "config": request.config}
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def run_job(job_id: str, db: Session):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        logger.error(f"Job {job_id} not found.")
        return
        
    job.status = "running"
    db.commit()
    
    try:
        problem_type = job.problem_type
        config_data = job.config
        
        problem = get_problem(problem_type, config_data["data"])
        Q = problem.to_qubo()
        
        for solver_name in config_data["solvers"]:
            solver = get_solver(solver_name)
            solver_config = config_data.get("config", {})
            
            logger.info(f"Running solver {solver_name} for job {job_id}")
            result_data = solver.solve(Q, solver_config)
            
            # Interpret solution
            interpreted_solution = problem.interpret_solution(result_data.best_solution)
            
            db_result = Result(
                job_id=job.id,
                solver_name=result_data.solver_name,
                best_solution=interpreted_solution,
                objective_value=result_data.objective_value,
                runtime_seconds=result_data.runtime_seconds,
                metadata=result_data.metadata
            )
            db.add(db_result)
            
        job.status = "completed"
        db.commit()
        logger.info(f"Job {job_id} completed successfully.")
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        logger.error(traceback.format_exc())
        job.status = "failed"
        job.error_message = str(e)
        db.commit()
