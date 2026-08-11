import json
import os
from datetime import datetime
from typing import Dict, Any

class ExperimentTracker:
    """
    A lightweight, MLflow-like experiment tracking module for AetherOpt.
    Logs parameters, metrics, and solver performance to a local store.
    """
    def __init__(self, log_dir: str = "experiments/runs"):
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
    def log_run(self, experiment_name: str, problem_type: str, params: Dict[str, Any], results: Dict[str, Any]):
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        run_data = {
            "run_id": run_id,
            "experiment": experiment_name,
            "problem": problem_type,
            "timestamp": datetime.utcnow().isoformat(),
            "parameters": params,
            "metrics": results
        }
        
        file_path = os.path.join(self.log_dir, f"{experiment_name}_{run_id}.json")
        with open(file_path, "w") as f:
            json.dump(run_data, f, indent=4)
            
        return run_id
