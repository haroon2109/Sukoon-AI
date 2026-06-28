from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# If a DATABASE_URL is provided (e.g. from GCP Secret Manager), use it (Postgres).
# Otherwise fallback to local SQLite for development.
if settings.DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    # For postgres we usually don't need connect_args={"check_same_thread": False}
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sukoon.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency to get a database session for a request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
