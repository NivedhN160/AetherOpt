from fastapi import APIRouter
import os
import json

router = APIRouter()

@router.get("/")
def list_experiments(limit: int = 50):
    log_dir = "experiments/runs"
    if not os.path.exists(log_dir):
        return []
        
    experiments = []
    files = sorted(os.listdir(log_dir), reverse=True)
    for filename in files[:limit]:
        if filename.endswith(".json"):
            with open(os.path.join(log_dir, filename), 'r') as f:
                try:
                    data = json.load(f)
                    # Don't send huge payloads if they just want a list, but for MVP it's fine.
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
