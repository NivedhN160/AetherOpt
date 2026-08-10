import pytest
import time
from fastapi.testclient import TestClient

def test_job_lifecycle(client: TestClient):
    # 1. Submit Job
    payload = {
        "problem_type": "portfolio",
        "data": {
            "expected_returns": [0.1, 0.2],
            "covariance_matrix": [[0.04, 0.01], [0.01, 0.05]],
            "k": 1,
            "risk_aversion": 0.5
        },
        "solvers": ["classical_sa", "highs"],
        "config": {"num_reads": 2, "num_steps": 10}
    }
    
    response = client.post(
        "/api/v1/jobs/",
        json=payload,
        headers={"X-API-Key": "secret_key"}
    )
    assert response.status_code == 202
    
    job_id = response.json()["id"]
    
    # 2. Poll until complete
    max_retries = 30
    for _ in range(max_retries):
        status_resp = client.get(
            f"/api/v1/results/{job_id}",
            headers={"X-API-Key": "secret_key"}
        )
        assert status_resp.status_code == 200
        
        status_data = status_resp.json()
        if status_data["status"] == "completed":
            break
        elif status_data["status"] == "failed":
            pytest.fail(f"Job failed: {status_data.get('error_message')}")
            
        time.sleep(0.1)
        
    assert status_data["status"] == "completed"
    assert len(status_data["results"]) == 2 # 2 solvers
