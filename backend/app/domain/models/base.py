from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

# Utility for generating standard UUID PKs
def generate_uuid():
    return str(uuid.uuid4())
