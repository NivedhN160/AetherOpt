import os
import shutil

dirs = [
    "aetheropt/solvers/classical",
    "aetheropt/solvers/quantum_inspired",
    "aetheropt/solvers/quantum",
    "aetheropt/solvers/hybrid",
    "aetheropt/crypto/primitives",
    "aetheropt/crypto/quantum_safe_optimization",
    "aetheropt/datascience/preprocessing",
    "aetheropt/datascience/feature_engineering",
    "aetheropt/datascience/experiments",
    "aetheropt/datascience/visualization",
    "aetheropt/datascience/ml_models",
    "benchmarks",
    "experiments",
    "notebooks"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    init_path = os.path.join(d, "__init__.py")
    if d.startswith("aetheropt") and not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            pass

# Move solvers
moves = {
    "aetheropt/solvers/classical_sa.py": "aetheropt/solvers/classical/classical_sa.py",
    "aetheropt/solvers/highs_solver.py": "aetheropt/solvers/classical/highs_solver.py",
    "aetheropt/solvers/quantum_inspired_sa.py": "aetheropt/solvers/quantum_inspired/quantum_inspired_sa.py",
    "aetheropt/solvers/qaoa_local.py": "aetheropt/solvers/quantum/qaoa.py",
}

for src, dst in moves.items():
    if os.path.exists(src):
        shutil.move(src, dst)
        print(f"Moved {src} to {dst}")
