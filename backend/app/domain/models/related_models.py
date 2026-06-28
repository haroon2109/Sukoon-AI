from sqlalchemy import Column, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
import datetime
from .base import Base, generate_uuid

class MediaAsset(Base):
    __tablename__ = "media_assets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    claim_id = Column(String(36), ForeignKey("claims.id", ondelete="CASCADE"), nullable=False)
    media_type = Column(String(50)) # video, image, audio
    storage_url = Column(String(512))
    file_hash = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    claim = relationship("Claim", back_populates="media_assets")

class EvidenceSource(Base):
    __tablename__ = "evidence_sources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    verification_id = Column(String(36), ForeignKey("verifications.id", ondelete="CASCADE"), nullable=False)
    source_name = Column(String(255))
    evidence_url = Column(String(512))
    snippet = Column(String(1024))
    match_confidence = Column(Float)

    # Relationships
    verification = relationship("Verification", back_populates="evidence_sources")

class RiskScore(Base):
    __tablename__ = "risk_scores"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    verification_id = Column(String(36), ForeignKey("verifications.id", ondelete="CASCADE"), nullable=False)
    toxicity_score = Column(Float)
    deepfake_probability = Column(Float)
    hate_speech_confidence = Column(Float)
    severity_level = Column(String(50)) # low, medium, high, critical

    # Relationships
    verification = relationship("Verification", back_populates="risk_scores")
