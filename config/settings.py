import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Quantis AI"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DATABASE_URL: str = "sqlite+aiosqlite:///./quantis.db"
    FETCH_INTERVAL_MINUTES: int = 30
    MIN_EDITORIAL_SCORE: float = 7.0

settings = Settings()
