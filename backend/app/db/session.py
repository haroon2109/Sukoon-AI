from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sukoon.db"

# Setting up the engine (using synchronous engine for simplicity in MVP, 
# though asyncpg could be used for production async database access)
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
