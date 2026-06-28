from sqlalchemy.orm import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

# Utility for generating standard UUID PKs
def generate_uuid():
    return str(uuid.uuid4())
