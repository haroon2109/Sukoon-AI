from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    CORS_ORIGINS: str = "http://localhost:3000,https://sukoon-ai-pied.vercel.app"

    @model_validator(mode="after")
    def validate_database_url(self) -> 'Settings':
        if not self.DATABASE_URL:
            if self.ENVIRONMENT == "development":
                # Fallback to local SQLite database to make development zero-config
                self.DATABASE_URL = "sqlite:///./sukoon.db"
            elif self.ENVIRONMENT != "testing":
                raise ValueError("DATABASE_URL must be specified in production/staging environments.")
        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
