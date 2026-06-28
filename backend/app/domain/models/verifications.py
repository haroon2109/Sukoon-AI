from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from .base import Base, generate_uuid

class Verification(Base):
    __tablename__ = "verifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    claim_id = Column(String(36), ForeignKey("claims.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="pending") # pending, processing, completed
    verdict = Column(String(50)) # verified, misleading, false
    generated_truth_card_url = Column(String(512))
    completed_at = Column(DateTime)

    # Relationships
    claim = relationship("Claim", back_populates="verifications")
    user = relationship("User", back_populates="verifications")
    evidence_sources = relationship("EvidenceSource", back_populates="verification", cascade="all, delete-orphan")
    risk_scores = relationship("RiskScore", back_populates="verification", cascade="all, delete-orphan")
