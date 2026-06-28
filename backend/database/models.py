import uuid
from datetime import datetime
from enum import Enum as PyEnum
from typing import List, Optional

from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    ForeignKey,
    Enum,
    Text,
    func,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class UserRole(str, PyEnum):
    USER = "user"
    ADMIN = "admin"

class SourcePlatform(str, PyEnum):
    WHATSAPP = "whatsapp"
    X = "x"
    INSTAGRAM = "instagram"

class RequestStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class MediaType(str, PyEnum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"

class Verdict(str, PyEnum):
    TRUE = "true"
    FALSE = "false"
    MISLEADING = "misleading"
    UNVERIFIED = "unverified"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    requests: Mapped[List["VerificationRequest"]] = relationship("VerificationRequest", back_populates="user", cascade="all, delete-orphan")
    api_keys: Mapped[List["ApiKey"]] = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")


class ApiKey(Base):
    """B2B Enterprise API Keys for programmatic access"""
    __tablename__ = "api_keys"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    key_prefix: Mapped[str] = mapped_column(String, nullable=False) # e.g. "sk_live_..."
    hashed_key: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String, default="Default Key")
    is_active: Mapped[bool] = mapped_column(default=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    last_used_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship("User", back_populates="api_keys")


class VerificationRequest(Base):
    __tablename__ = "verification_requests"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    source_platform: Mapped[SourcePlatform] = mapped_column(Enum(SourcePlatform), nullable=False)
    status: Mapped[RequestStatus] = mapped_column(Enum(RequestStatus), default=RequestStatus.PENDING, index=True, nullable=False)
    original_content: Mapped[Optional[str]] = mapped_column(Text)
    
    # Edge Caching Strategy fields
    content_hash: Mapped[Optional[str]] = mapped_column(String, index=True) 
    is_cached_result: Mapped[bool] = mapped_column(default=False)
    
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="requests")
    media_assets: Mapped[List["MediaAsset"]] = relationship("MediaAsset", back_populates="request", cascade="all, delete-orphan")
    claims: Mapped[List["Claim"]] = relationship("Claim", back_populates="request", cascade="all, delete-orphan")
    risk_score: Mapped["RiskScore"] = relationship("RiskScore", back_populates="request", cascade="all, delete-orphan", uselist=False)
    agent_outputs: Mapped[List["AgentOutput"]] = relationship("AgentOutput", back_populates="request", cascade="all, delete-orphan")


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("verification_requests.id", ondelete="CASCADE"), index=True)
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_hash: Mapped[str] = mapped_column(String, index=True)  # Hash index would be configured at DB level
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    request: Mapped["VerificationRequest"] = relationship("VerificationRequest", back_populates="media_assets")


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("verification_requests.id", ondelete="CASCADE"), index=True)
    claim_text: Mapped[str] = mapped_column(Text, nullable=False)
    entities: Mapped[Optional[dict]] = mapped_column(JSONB) # GIN index typically configured manually in alembic
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    request: Mapped["VerificationRequest"] = relationship("VerificationRequest", back_populates="claims")
    fact_checks: Mapped[List["FactCheck"]] = relationship("FactCheck", back_populates="claim", cascade="all, delete-orphan")


class FactCheck(Base):
    __tablename__ = "fact_checks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    claim_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("claims.id", ondelete="CASCADE"), index=True)
    verdict: Mapped[Verdict] = mapped_column(Enum(Verdict), default=Verdict.UNVERIFIED, index=True, nullable=False)
    matched_context: Mapped[Optional[str]] = mapped_column(Text)
    source_urls: Mapped[Optional[List[str]]] = mapped_column(JSONB)
    peace_message: Mapped[Optional[str]] = mapped_column(Text)
    
    verified_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    claim: Mapped["Claim"] = relationship("Claim", back_populates="fact_checks")


class RiskScore(Base):
    __tablename__ = "risk_scores"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("verification_requests.id", ondelete="CASCADE"), unique=True, index=True)
    toxicity_score: Mapped[Optional[float]] = mapped_column(Float, index=True)
    hate_speech_score: Mapped[Optional[float]] = mapped_column(Float, index=True)
    flagged_dog_whistles: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    computed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    request: Mapped["VerificationRequest"] = relationship("VerificationRequest", back_populates="risk_score")


class AgentOutput(Base):
    __tablename__ = "agent_outputs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("verification_requests.id", ondelete="CASCADE"), index=True)
    agent_name: Mapped[str] = mapped_column(String, nullable=False)
    raw_output: Mapped[Optional[dict]] = mapped_column(JSONB)
    confidence_score: Mapped[Optional[float]] = mapped_column(Float)
    processing_time_ms: Mapped[Optional[int]] = mapped_column(Integer)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    request: Mapped["VerificationRequest"] = relationship("VerificationRequest", back_populates="agent_outputs")
