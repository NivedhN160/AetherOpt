import json
import os

def main():
    print("Generating sample problem data...")
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples", "sample_data")
    os.makedirs(data_dir, exist_ok=True)
    
    portfolio_data = {
        "expected_returns": [0.05, 0.10, 0.12, 0.08, 0.15],
        "covariance_matrix": [
            [0.01, 0.005, 0.002, 0.001, 0.008],
            [0.005, 0.02, 0.01, 0.003, 0.01],
            [0.002, 0.01, 0.03, 0.005, 0.012],
            [0.001, 0.003, 0.005, 0.015, 0.004],
            [0.008, 0.01, 0.012, 0.004, 0.04]
        ],
        "k": 2,
        "risk_aversion": 0.5
    }
    
    with open(os.path.join(data_dir, "portfolio_sample.json"), "w") as f:
        json.dump(portfolio_data, f, indent=2)
        
    print(f"Sample data generated in {data_dir}")

if __name__ == "__main__":
    main()
