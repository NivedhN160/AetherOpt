def generate_energy_plot_data(energies: list) -> dict:
    """
    Generates data structure suitable for plotting energy over time 
    in a frontend charting library like Chart.js or Plotly.
    """
    return {
        "labels": list(range(len(energies))),
        "datasets": [
            {
                "label": "Energy",
                "data": energies,
                "borderColor": "#3b82f6",
                "fill": False
            }
        ]
    }
