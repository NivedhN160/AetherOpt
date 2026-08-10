# AetherOpt

**Production-Grade Quantum-Inspired Optimization Platform**

AetherOpt is an end-to-end framework and API for mapping hard combinatorial problems to Quadratic Unconstrained Binary Optimization (QUBO) and solving them using classical, quantum-inspired, and exact solvers. 

It is designed with stability, asynchronous execution, and rigorous data validation to serve as a robust backend for production workloads.

## Features

- **Asynchronous Execution:** Safely run long combinatorial solves in the background with a thread-safe SQLAlchemy integration.
- **Strict Data Validation:** Comprehensive Pydantic models for all problem domains (Portfolio, Max-Cut, Routing, Scheduling) ensuring fail-fast validation.
- **Multiple Solvers:**
  - `quantum_inspired_sa`: Simulated annealing enhanced with barrier tunneling probability bounds.
  - `classical_sa`: Fast, traditional simulated annealing.
  - `highs`: High-performance mixed-integer programming (MIP) exact solver via HiGHS, with guardrails on problem size.
- **Job History:** View and poll past optimization runs with full energy histories and solver metadata.
- **Modern UI:** Built-in SPA (Alpine.js + TailwindCSS) demonstrating all problem formulations and real-time polling.

## Getting Started

### Installation

1. Clone the repository.
2. Ensure you have `uv` installed. If not: `pip install uv`
3. Sync dependencies: `uv sync`

### Running the App

Start the application with both the frontend and API exposed on port 8000:

```bash
npm start
```
*Note: This runs `uv run aetheropt` under the hood.*

Visit `http://localhost:8000` to access the interactive web interface.
The API Documentation is available at `http://localhost:8000/docs`.

### API Usage Example

Submit a Portfolio Optimization job to the exact solver and quantum-inspired SA:

```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/jobs/' \
  -H 'accept: application/json' \
  -H 'X-API-Key: secret_key' \
  -H 'Content-Type: application/json' \
  -d '{
  "problem_type": "portfolio",
  "data": {
    "expected_returns": [0.1, 0.2],
    "covariance_matrix": [[0.04, 0.01], [0.01, 0.05]],
    "k": 1,
    "risk_aversion": 0.5
  },
  "solvers": [
    "quantum_inspired_sa",
    "highs"
  ],
  "config": {
    "num_reads": 10,
    "num_steps": 1000,
    "seed": 42
  }
}'
```

## Running Tests

Execute the comprehensive test suite locally:

```bash
uv run pytest
```
