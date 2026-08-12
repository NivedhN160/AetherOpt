import numpy as np
from typing import List, Dict

class ResultAnalyzer:
    """
    Computes statistical properties across multiple solver runs.
    """
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
