from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    api_key: str = "secret_key"
    database_url: str = "sqlite:///./aetheropt.db"
    aetheropt_env: str = "development"
    cors_origins: List[str] = ["*"]
    max_qubo_size: int = 200
    
    # Research settings
    quantum_backend: str = "aer_simulator"
    max_qaoa_qubits: int = 18
    enable_crypto: bool = True
    experiment_tracking: bool = True
    ds_pipeline_enabled: bool = True
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
