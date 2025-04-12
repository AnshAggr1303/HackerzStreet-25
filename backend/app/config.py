# config/config.py
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Insurance RAG API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Multilingual Insurance RAG System with Llama Integration"
    
    # Path settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    EMBEDDINGS_DIR: Path = BASE_DIR / "embeddings_output"
    DATA_DIR: Path = BASE_DIR / "data"
    
    # Service settings
    LIBRE_TRANSLATE_URL: str = "http://localhost:5000"
    OLLAMA_URL: str = "http://localhost:11434"
    
    # RAG settings
    TOP_K_RESULTS: int = 3
    CHUNK_SIZE: int = 512
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()