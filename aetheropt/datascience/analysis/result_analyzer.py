import numpy as np
from typing import List, Dict

class ResultAnalyzer:
    """
    Computes statistical properties across multiple solver runs.
    """
    def __init__(self, log_dir: str = "experiments/runs"):
        self.log_dir = log_dir

    @staticmethod
    def compare_solvers(results: List[Dict]) -> dict:
        """
        Given a list of solver result dicts (from an experiment JSON),
        compute comparative statistics.
        """
        analysis = {}
        for res in results:
            name = res.get("solver_name", "unknown")
            energy = res.get("objective_value", float('inf'))
            time = res.get("runtime_seconds", 0)
            
            analysis[name] = {
                "energy": energy,
                "time": time
            }
            
            meta = res.get("solver_metadata", {})
            if "energies" in meta and len(meta["energies"]) > 0:
                energies = meta["energies"]
                analysis[name].update({
                    "mean_energy": np.mean(energies),
                    "std_energy": np.std(energies),
                    "best_energy": np.min(energies)
                })
        return analysis

    def generate_summary(self) -> dict:
        """
        Scans all experiment JSONs and generates overall statistics.
        """
        import os
        import json
        
        if not os.path.exists(self.log_dir):
            return {"total_experiments": 0}
            
        total_experiments = 0
        best_overall_energy = float('inf')
        total_runtime = 0.0
        problem_types = {}
        solver_wins = {}
        
        for filename in os.listdir(self.log_dir):
            if filename.endswith(".json"):
                total_experiments += 1
                try:
                    with open(os.path.join(self.log_dir, filename), 'r') as f:
                        data = json.load(f)
                        
                    ptype = data.get("problem_type", "unknown")
                    problem_types[ptype] = problem_types.get(ptype, 0) + 1
                    
                    results = data.get("results", [])
                    if not results: continue
                    
                    # Find best solver in this run
                    best_run_energy = float('inf')
                    best_solver = None
                    for res in results:
                        energy = res.get("objective_value", float('inf'))
                        runtime = res.get("runtime_seconds", 0)
                        total_runtime += runtime
                        
                        if energy < best_run_energy:
                            best_run_energy = energy
                            best_solver = res.get("solver_name", "unknown")
                            
                        if energy < best_overall_energy:
                            best_overall_energy = energy
                            
                    if best_solver:
                        solver_wins[best_solver] = solver_wins.get(best_solver, 0) + 1
                        
                except Exception:
                    pass
                    
        return {
            "total_experiments": total_experiments,
            "best_overall_energy": best_overall_energy if best_overall_energy != float('inf') else None,
            "average_runtime": total_runtime / total_experiments if total_experiments > 0 else 0,
            "problem_type_distribution": problem_types,
            "solver_wins": solver_wins
        }
