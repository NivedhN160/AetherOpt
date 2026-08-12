from fastapi import APIRouter
import os
import json

router = APIRouter()

from typing import Optional

@router.get("/")
def list_experiments(
    limit: int = 50,
    problem_type: Optional[str] = None,
    solver: Optional[str] = None
):
    log_dir = "experiments/runs"
    if not os.path.exists(log_dir):
        return []
        
    experiments = []
    files = sorted(os.listdir(log_dir), reverse=True)
    for filename in files:
        if len(experiments) >= limit:
            break
            
        if filename.endswith(".json"):
            with open(os.path.join(log_dir, filename), 'r') as f:
                try:
                    data = json.load(f)
                    
                    if problem_type and data.get("problem_type") != problem_type:
                        continue
                        
                    if solver and solver not in data.get("solvers", []):
                        continue
                        
                    experiments.append(data)
                except Exception:
                    pass
    return experiments

@router.get("/{run_id}")
def get_experiment(run_id: str):
    log_dir = "experiments/runs"
    filepath = os.path.join(log_dir, f"{run_id}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {"error": "Experiment not found"}
