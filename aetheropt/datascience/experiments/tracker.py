import json
import os
import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ExperimentTracker:
    """
    Logs optimization runs, configurations, and results for analytics.
    """
    def __init__(self, log_dir: str = "experiments/runs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
    def log_run(self, job_id: str, problem_type: str, solvers_used: list, config: Dict[str, Any], results: list):
        """
        Saves a rich JSON payload describing the run.
        """
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        run_id = f"job_{job_id}_{timestamp}"
        
        payload = {
            "run_id": run_id,
            "job_id": job_id,
            "problem_type": problem_type,
            "timestamp": timestamp,
            "config": config,
            "solvers": solvers_used,
            "results": results
        }
        
        filepath = os.path.join(self.log_dir, f"{run_id}.json")
        try:
            with open(filepath, 'w') as f:
                json.dump(payload, f, indent=2)
            logger.info(f"Experiment saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to log experiment: {e}")
