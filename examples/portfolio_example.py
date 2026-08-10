import requests
import time
import json

def run_example():
    print("Submitting Portfolio Job to AetherOpt...")
    response = requests.post("http://localhost:8000/api/v1/jobs/", json={
        "problem_type": "portfolio",
        "data": {
            "expected_returns": [0.1, 0.15, 0.08, 0.2],
            "covariance_matrix": [
                [0.04, 0.01, 0.0, 0.0],
                [0.01, 0.06, 0.02, 0.0],
                [0.0, 0.02, 0.03, 0.01],
                [0.0, 0.0, 0.01, 0.08]
            ],
            "k": 2,
            "risk_aversion": 0.5
        },
        "solvers": ["quantum_inspired_sa", "classical_sa", "highs", "qaoa_local"],
        "config": {"num_reads": 10, "num_steps": 200}
    }, headers={"X-API-Key": "secret_key"})
    
    if response.status_code != 200:
        print("Failed to submit job:", response.text)
        return
        
    job_id = response.json()["id"]
    print(f"Job ID: {job_id}")
    
    while True:
        status_resp = requests.get(f"http://localhost:8000/api/v1/results/{job_id}", headers={"X-API-Key": "secret_key"})
        status_data = status_resp.json()
        status = status_data["status"]
        print(f"Status: {status}")
        
        if status in ["completed", "failed"]:
            print(json.dumps(status_data, indent=2))
            break
            
        time.sleep(1)

if __name__ == "__main__":
    run_example()
