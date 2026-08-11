import json
import os
import matplotlib.pyplot as plt
from typing import Dict, Any

def plot_energy_landscape(experiment_json_path: str, output_image_path: str = None):
    """
    Plots the energy landscape/descent from a given experiment run file.
    Assumes the solver logged an 'energies' array in its metadata.
    """
    if not os.path.exists(experiment_json_path):
        raise FileNotFoundError(f"Experiment file {experiment_json_path} not found.")
        
    with open(experiment_json_path, 'r') as f:
        data = json.load(f)
        
    metadata = data.get("metrics", {}).get("metadata", {})
    energies = metadata.get("energies", [])
    
    if not energies:
        print(f"No energy descent data found in {experiment_json_path}")
        return
        
    plt.figure(figsize=(10, 6))
    plt.plot(energies, color='#00aaff', linewidth=2)
    plt.title(f"Energy Landscape Descent - {data.get('problem', 'Unknown')} / {data.get('parameters', {}).get('solver', 'Solver')}")
    plt.xlabel("Iteration / Step")
    plt.ylabel("Objective Energy")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if output_image_path:
        plt.savefig(output_image_path, dpi=300)
        print(f"Plot saved to {output_image_path}")
    else:
        plt.show()
