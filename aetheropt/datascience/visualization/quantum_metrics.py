import matplotlib.pyplot as plt
import numpy as np
from typing import List

def plot_quantum_probabilities(states: List[str], probabilities: List[float], output_image_path: str = None):
    """
    Plots a histogram of quantum state probabilities (e.g., from a QAOA state vector).
    """
    if len(states) != len(probabilities):
        raise ValueError("Length of states and probabilities must match.")
        
    plt.figure(figsize=(12, 6))
    
    # Sort by probability for better visualization
    sorted_indices = np.argsort(probabilities)[::-1][:20] # Top 20 states
    top_states = [states[i] for i in sorted_indices]
    top_probs = [probabilities[i] for i in sorted_indices]
    
    x_pos = np.arange(len(top_states))
    
    plt.bar(x_pos, top_probs, color='#8800ff', alpha=0.8)
    plt.xticks(x_pos, top_states, rotation=45, ha='right')
    plt.title("Quantum State Probabilities (Top 20)")
    plt.xlabel("Basis State")
    plt.ylabel("Probability")
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    if output_image_path:
        plt.savefig(output_image_path, dpi=300)
        print(f"Plot saved to {output_image_path}")
    else:
        plt.show()
