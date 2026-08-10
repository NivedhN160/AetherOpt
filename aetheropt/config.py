from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    api_key: str = "secret_key"
    database_url: str = "sqlite:///./aetheropt.db"
    aetheropt_env: str = "development"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
