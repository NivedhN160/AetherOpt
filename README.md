<div align="center">
  <a href="README.md"><b>📖 README</b></a> &nbsp; | &nbsp;
  <a href="architecture.md"><b>🏗️ Architecture</b></a> &nbsp; | &nbsp;
  <a href="do.md"><b>📋 Project Spec</b></a> &nbsp; | &nbsp;
  <a href="LICENSE.md"><b>⚖️ License</b></a>
</div>

<br/>

<div align="center">
  <h1>AetherOpt 🌌</h1>
  <p><b>Production-Grade Quantum-Inspired Optimization Platform</b></p>
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite" />
</div>

<br/>

AetherOpt is an end-to-end framework and API for mapping hard combinatorial problems to Quadratic Unconstrained Binary Optimization (QUBO) and solving them using classical, quantum-inspired, and exact solvers. 

It is designed with stability, asynchronous execution, and rigorous data validation to serve as a robust backend for production workloads.

---

## 📸 Interactive Web Interface

![AetherOpt Dashboard](assets/screenshot_home.png)

![AetherOpt Results](assets/screenshot_results.png)

---

## 🚀 Features

- **Asynchronous Execution:** Safely run long combinatorial solves in the background with a thread-safe SQLAlchemy integration.
- **Strict Data Validation:** Comprehensive Pydantic models for all problem domains (Portfolio, Max-Cut, Routing, Scheduling) ensuring fail-fast validation.
- **Multiple Solvers:**
  - 🔮 `quantum_inspired_sa`: Simulated annealing enhanced with barrier tunneling probability bounds.
  - ⚙️ `classical_sa`: Fast, traditional simulated annealing.
  - 📏 `highs`: High-performance mixed-integer programming (MIP) exact solver via HiGHS, with guardrails on problem size.
- **Job History:** View and poll past optimization runs with full energy histories and solver metadata.
- **Interactive UI:** Built-in SPA (Alpine.js + TailwindCSS) demonstrating all problem formulations and real-time polling.

---

## 🛠️ Getting Started

### 1. Installation

Clone the repository and ensure you have `uv` installed (if not: `pip install uv`).

```bash
uv sync
```

### 2. Run the Server

Start the application with both the frontend and API exposed on port 8000:

```bash
npm start
```
*(This automatically runs `uv run aetheropt`)*

### 3. Interactive Web UI
Visit [http://localhost:8000](http://localhost:8000) to access the interactive web interface, where you can define matrices and submit jobs seamlessly.

---

## 📚 Interactive API Usage

You can also submit jobs directly via curl. Try out this Portfolio Optimization problem!

<details>
<summary><b>Show cURL Example</b></summary>

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

</details>

After receiving a Job ID, poll the results:

```bash
curl -H 'X-API-Key: secret_key' http://localhost:8000/api/v1/results/{YOUR_JOB_ID}
```

---

## 🏗️ Architecture

Curious about how AetherOpt processes jobs and maps domains to QUBOs? 
👉 **Check out the [Architecture Overview](architecture.md).**

## 🧪 Testing

Execute the comprehensive test suite locally:

```bash
uv run pytest
```
