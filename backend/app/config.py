from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/financial_ai"
    secret_key: str = "SECRET_KEY"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    upload_dir: str = "uploads"
    class Config:
        env_file = ".env"
settings = Settings()
