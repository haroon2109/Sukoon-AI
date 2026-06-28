from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    QDRANT_URL: str | None = None
    QDRANT_API_KEY: str | None = None
    GCP_PROJECT_ID: str = "arenagrid"
    GCP_REGION: str = "us-central1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
