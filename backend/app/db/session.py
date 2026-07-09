from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# If a DATABASE_URL is provided (e.g. from GCP Secret Manager), use it (Postgres).
# Otherwise fallback to local SQLite for development.
import os

if settings.DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    # Render provides URLs starting with 'postgres://', but SQLAlchemy 1.4+ requires 'postgresql://'
    if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)
        
    # For postgres we usually don't need connect_args={"check_same_thread": False}
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
else:
    data_dir = os.getenv("DATA_DIR", ".")
    db_path = os.path.join(data_dir, "sukoon.db")
    # For absolute paths in Windows or Linux, sqlite URL requires ///
    # os.path.join might create backslashes on Windows, which sqlalchemy handles fine, but let's be safe:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path.replace(chr(92), '/')}"
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
