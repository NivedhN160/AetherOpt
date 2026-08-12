def prepare_energy_history_chart_data(results: list) -> dict:
    """
    Transforms a list of solver results into a format easily consumable by Chart.js.
    Extracts the 'energies' history from metadata.
    """
    datasets = []
    max_len = 0
    
    for res in results:
        name = res.get("solver_name", "unknown")
        meta = res.get("solver_metadata", {})
        if "energies" in meta and len(meta["energies"]) > 0:
            energies = meta["energies"]
            datasets.append({
                "label": name,
                "data": energies,
                "fill": False,
                "tension": 0.1
            })
            if len(energies) > max_len:
                max_len = len(energies)
                
    labels = list(range(max_len))
    
    return {
        "labels": labels,
        "datasets": datasets
    }
