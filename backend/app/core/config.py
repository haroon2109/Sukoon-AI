from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str | None = None
    GCP_PROJECT_ID: str = "arenagrid"
    GCP_REGION: str = "us-central1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str | None = None
    ENVIRONMENT: str = "development"
    SUPABASE_URL: str | None = None
    SUPABASE_KEY: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
