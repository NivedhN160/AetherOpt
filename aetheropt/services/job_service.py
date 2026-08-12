import uuid
import datetime
from sqlalchemy.orm import Session
from aetheropt.db.models import Job, Result
from aetheropt.models.problem import ProblemRequest
from aetheropt.problems import get_problem
from aetheropt.solvers.registry import get_solver
from aetheropt.core.logging import logger
from aetheropt.config import settings
from aetheropt.crypto.secure_qubo import SecureQUBO
from aetheropt.crypto.commitments import ProblemCommitment
from aetheropt.crypto.verification import ResultVerification
from aetheropt.datascience.experiments.tracker import ExperimentTracker
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
                
                # 1. Generate Commitment
                problem_dict = {"Q": Q.tolist()}
                commitment = ProblemCommitment(problem_dict)
                commitment_payload = commitment.get_commitment_payload()
                config_data["commitment"] = commitment_payload
                
                # 2. Blind Matrix
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
                
                # Decode and Verify if crypto was used
                is_verified = None
                if use_crypto and len(result_data.best_solution) > 0:
                    import numpy as np
                    
                    # 1. Decode Permutation
                    decoded_state = secure_qubo.decode_solution(result_data.best_solution)
                    
                    # 2. Decode Energy
                    result_data.objective_value = secure_qubo.decode_energy(result_data.objective_value, decoded_state)
                    
                    # 3. Verify
                    is_verified = ResultVerification.verify_solution(
                        problem_data={"Q": Q.tolist()},
                        nonce=config_data["commitment"]["nonce"],
                        commitment=config_data["commitment"]["commitment"],
                        solution=decoded_state,
                        q_matrix=Q,
                        reported_energy=result_data.objective_value
                    )
                    result_data.solver_metadata["crypto_verified"] = is_verified
                    
                    result_data.best_solution = decoded_state
                
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
                all_results = []
                for res in db.query(Result).filter(Result.job_id == job_id).all():
                    all_results.append({
                        "solver_name": res.solver_name,
                        "best_solution": res.best_solution,
                        "objective_value": res.objective_value,
                        "runtime_seconds": res.runtime_seconds,
                        "solver_metadata": res.solver_metadata
                    })
                tracker.log_run(
                    job_id=job_id,
                    problem_type=problem_type,
                    solvers_used=config_data["solvers"],
                    config=config_data,
                    results=all_results
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
