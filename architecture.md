<div align="center">
  <a href="README.md"><b>📖 README</b></a> &nbsp; | &nbsp;
  <a href="architecture.md"><b>🏗️ Architecture</b></a> &nbsp; | &nbsp;
  <a href="do.md"><b>📋 Project Spec</b></a> &nbsp; | &nbsp;
  <a href="LICENSE.md"><b>⚖️ License</b></a>
</div>

<br/>

# AetherOpt Architecture

AetherOpt is structured as a modern, asynchronous, Python-based API designed for combinatorial optimization workloads. It bridges the gap between quantum-inspired algorithms and classical operations research by providing a unified interface to formulate and solve NP-hard problems.

## System Overview

```mermaid
graph TD
    UI[Alpine.js / HTMX Frontend] --> API[FastAPI Endpoints]
    API --> JobService[Job Service]
    JobService --> DB[(SQLite Database)]
    JobService --> Background[Background Task Runner]
    Background --> Registry[Solver Registry]
    Registry --> SA[Simulated Annealing]
    Registry --> QISA[Quantum-Inspired SA]
    Registry --> Highs[HiGHS Exact Solver]
    Background --> DB
```

## Core Components

### 1. API Layer (`aetheropt/api/`)
FastAPI routers handling incoming HTTP requests. Models are validated using Pydantic, ensuring strictly typed data before it reaches the core system.

### 2. Validation & Security (`aetheropt/core/` and `aetheropt/crypto/`)
Problems are validated, API Keys are checked, and optional quantum-safe cryptography operations (e.g., QUBO coefficient encryption) are applied.

### 3. Data Science Pipeline (`aetheropt/datascience/`)
An integrated pipeline for feature engineering, pre-processing, ML surrogate models, and rigorous experiment tracking.

### 4. Background Job Management (`aetheropt/services/job_service.py`)
Heavy lifting is offloaded to `BackgroundTasks`. The service retrieves the problem payload and pushes it to the solver orchestrator, logging status to SQLite.

### 5. Multi-Paradigm Solvers (`aetheropt/solvers/`)
The solver engine features four primary domains:
- **Classical**: Exact solvers (HiGHS) and classical SA.
- **Quantum-Inspired**: High-performance classical heuristic simulators (Simulated Bifurcation, PT).
- **Quantum**: State-vector QAOA and VQE simulators (Qiskit Aer).
- **Hybrid**: Quantum warm-starts followed by classical refinement.

### 6. Domain Models (`aetheropt/problems/`)
All real-world combinatorial problems are mapped into Quadratic Unconstrained Binary Optimization (QUBO) structures.
- **Portfolio Optimization**: Maps covariance and expected returns to a QUBO maximizing returns while penalizing risk.
- **Vehicle Routing & Scheduling**: Constrained graphs reduced to binary penalties.
- **Max-Cut**: Standard graph partitioning formulation.

### 3. Solver Registry (`aetheropt/solvers/`)
All solvers inherit from `BaseSolver` and implement a `.solve(Q, config)` method, returning a unified `SolverResultData`.
- **Classical SA**: Pure simulated annealing.
- **Quantum-Inspired SA**: Simulated annealing incorporating quantum tunneling approximations to escape local minima, bounded by barrier heights.
- **HiGHS Solver**: Translates QUBOs into Mixed Integer Programming (MIP) problems. Highs provides exact verification for smaller problem sizes ($n < 100$).

### 4. Background Execution & State Management
Combinatorial solving is CPU-bound and blocks the event loop.
- **FastAPI BackgroundTasks** dispatches solvers to a separate thread.
- **Database Thread Safety**: We use a `get_db_session()` context manager inside the background workers to ensure SQLAlchemy `Session` objects are strictly isolated per-thread, avoiding silent SQLite crashes.

## Project Structure

```
AetherOpt/
├── aetheropt/
│   ├── api/          # FastAPI Routes (Jobs, Results)
│   ├── core/         # Security, Dependencies
│   ├── db/           # SQLAlchemy Models, Session Engine
│   ├── models/       # Pydantic Schemas (Strict Validation)
│   ├── problems/     # QUBO Formulations (Portfolio, Routing...)
│   ├── services/     # Job orchestration and db logic
│   ├── solvers/      # The algorithmic cores (SA, Highs)
│   ├── static/       # Alpine.js Frontend UI
│   └── main.py       # Application Entrypoint
├── tests/            # Pytest Suite (Unit & E2E)
├── config.py         # Environment configuration
└── pyproject.toml    # uv / python metadata
```

## Concurrency Model
AetherOpt handles synchronous requests quickly by persisting a `Job` record in `pending` status. The background task modifies the state to `running`, executes the solvers in series (or parallel, in future iterations), and commits the `completed` state containing a JSON serialization of all solver metadata and execution times.
