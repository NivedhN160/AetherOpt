import uuid
import datetime
from sqlalchemy.orm import Session
from aetheropt.db.models import Job, Result
from aetheropt.models.problem import ProblemRequest
from aetheropt.problems import get_problem
from aetheropt.solvers.registry import get_solver
from aetheropt.core.logging import logger
from aetheropt.config import settings
from aetheropt.crypto.quantum_safe_optimization.secure_qubo import SecureQUBO
from aetheropt.datascience.experiments.experiment_tracker import ExperimentTracker
import traceback

def create_job(db: Session, request: ProblemRequest) -> Job:
    job_id = str(uuid.uuid4())
    job = Job(
        id=job_id,
        problem_type=request.problem_type,
        status="pending",
        config={"data": request.data.model_dump(), "solvers": request.solvers, "config": request.config}
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

from aetheropt.db.session import get_db_session

def run_job(job_id: str):
    with get_db_session() as db:
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
            
            # Crypto / Secure QUBO check
            use_crypto = settings.enable_crypto or config_data.get("config", {}).get("secure", False)
            if use_crypto:
                logger.info(f"Applying SecureQUBO blinding for job {job_id}")
                secure_qubo = SecureQUBO(Q)
                Q_run = secure_qubo.blind_matrix()
            else:
                Q_run = Q
            
            tracker = None
            if settings.experiment_tracking:
                tracker = ExperimentTracker()

            for solver_name in config_data["solvers"]:
                solver = get_solver(solver_name)
                solver_config = config_data.get("config", {})
                
                logger.info(f"Running solver {solver_name} for job {job_id}")
                result_data = solver.solve(Q_run, solver_config)
                
                # Decode if crypto was used
                if use_crypto and len(result_data.best_solution) > 0:
                    import numpy as np
                    state = np.array(result_data.best_solution)
                    result_data.objective_value = secure_qubo.decode_energy(result_data.objective_value, state)
                
                # Interpret solution
                interpreted_solution = problem.interpret_solution(result_data.best_solution)
                
                db_result = Result(
                    job_id=job.id,
                    solver_name=result_data.solver_name,
                    best_solution=interpreted_solution,
                    objective_value=result_data.objective_value,
                    runtime_seconds=result_data.runtime_seconds,
                    solver_metadata=result_data.solver_metadata
                )
                db.add(db_result)
                
                # Experiment Tracking
                if tracker:
                    tracker.log_run(
                        experiment_name=f"job_{job_id}",
                        problem_type=problem_type,
                        params={"solver": solver_name, "config": solver_config, "use_crypto": use_crypto},
                        results={
                            "objective": result_data.objective_value,
                            "runtime": result_data.runtime_seconds,
                            "metadata": result_data.solver_metadata
                        }
                    )
                
            job.status = "completed"
            db.commit()
            logger.info(f"Job {job_id} completed successfully.")
            
        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}")
            logger.error(traceback.format_exc())
            job.status = "failed"
            job.error_message = str(e)
            db.commit()
