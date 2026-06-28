from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
import datetime
from .base import Base, generate_uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    api_key = Column(String(255), unique=True, index=True, nullable=False)
    organization_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    claims = relationship("Claim", back_populates="user", cascade="all, delete-orphan")
    verifications = relationship("Verification", back_populates="user", cascade="all, delete-orphan")
