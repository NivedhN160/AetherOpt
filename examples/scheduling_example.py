import requests
import time
import json

def run_example():
    print("Submitting Scheduling Job to AetherOpt...")
    response = requests.post("http://localhost:8000/api/v1/jobs/", json={
        "problem_type": "scheduling",
        "data": {
            "num_tasks": 5,
            "num_machines": 2,
            "task_lengths": [10, 20, 15, 5, 25]
        },
        "solvers": ["quantum_inspired_sa", "classical_sa"],
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
