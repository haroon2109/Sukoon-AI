from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from .base import Base, generate_uuid

class Claim(Base):
    __tablename__ = "claims"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    raw_content = Column(Text, nullable=False)
    extracted_claim = Column(Text)
    language = Column(String(10), default="en")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="claims")
    media_assets = relationship("MediaAsset", back_populates="claim", cascade="all, delete-orphan")
    verifications = relationship("Verification", back_populates="claim", cascade="all, delete-orphan")
