# AetherOpt

**Production-grade Quantum-Inspired Optimization Platform**

AetherOpt is a fully local, free, production-quality platform for solving combinatorial optimization problems using quantum-inspired algorithms and classical solvers.

## Features
- Portfolio Optimization
- Task Scheduling
- Vehicle Routing (small instances)
- Max-Cut
- Generic QUBO
- Quantum-Inspired Simulated Annealing
- Classical solvers (HiGHS)
- Optional local QAOA
- Clean web UI + REST API
- Job history & comparison
- Zero cost, runs on laptop

## Quick Start

```bash
git clone <repo>
cd aetheropt
python -m venv .venv
source .venv/bin/activate          # or .venv\Scripts\activate on Windows
pip install -e .
cp .env.example .env
aetheropt                         # or uvicorn aetheropt.main:app --reload
```

Open http://localhost:8000

## Architecture
AetherOpt runs as a FastAPI application with a SQLite database for jobs and results. Background tasks handle solver execution so the API remains responsive.

## Supported Problems
- Portfolio Optimization
- Task Scheduling
- Vehicle Routing
- Max-Cut
- Generic QUBO

## Solvers
- Quantum-Inspired SA (with tunneling)
- Classical SA
- HiGHS (Exact / Classical)
- Local QAOA (Placeholder for extension)

## API Documentation
http://localhost:8000/docs

## Configuration
See `.env.example`

## License
MIT
