from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Base paths
    BASE_DIR: Path = Path(__file__).parent
    STORAGE_DIR: Path = BASE_DIR / "data"
    
    # Database
    DB_PATH: Path = STORAGE_DIR / "financial_data.duckdb"
    
    # Vector Store
    VECTOR_INDEX_PATH: Path = STORAGE_DIR / "vector_index.faiss"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"  # Local, efficient model
    
    # Agent
    LLM_MODEL_NAME: str = "gpt-4-turbo" # Or local "mistral"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure storage directory exists
settings.STORAGE_DIR.mkdir(exist_ok=True)
