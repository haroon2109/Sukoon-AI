from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum
import bleach

# --- Enums ---
class SourcePlatform(str, Enum):
    TWITTER = "twitter"
    INSTAGRAM = "instagram"
    WHATSAPP = "whatsapp"
    FACEBOOK = "facebook"
    YOUTUBE = "youtube"
    OTHER = "other"

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    organization_name: Optional[str] = Field(None, max_length=100)
    
    @field_validator("organization_name")
    def sanitize_org_name(cls, v):
        if v is not None:
            return bleach.clean(v, strip=True)
        return v

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=128)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(UserBase):
    id: str
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Verification Requests ---
class UrlVerificationRequest(BaseModel):
    url: HttpUrl
    source_platform: SourcePlatform

# --- Claim Schemas ---
class ClaimCreate(BaseModel):
    raw_content: str = Field(..., min_length=1, max_length=5000)
    language: Optional[str] = Field("en", max_length=10)
    
    @field_validator("raw_content")
    def sanitize_content(cls, v):
        return bleach.clean(v, strip=True)

class ClaimResponse(BaseModel):
    id: str
    user_id: str
    raw_content: str
    extracted_claim: Optional[str]
    language: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Verification Schemas ---
class EvidenceSourceSchema(BaseModel):
    source_name: str
    evidence_url: Optional[str]
    snippet: Optional[str]
    match_confidence: float
    
    class Config:
        from_attributes = True

class RiskScoreSchema(BaseModel):
    toxicity_score: float
    deepfake_probability: float
    hate_speech_confidence: float
    severity_level: str
    
    class Config:
        from_attributes = True

class VerificationResponse(BaseModel):
    id: str
    claim_id: str
    status: str
    verdict: Optional[str]
    generated_truth_card_url: Optional[str]
    evidence_sources: List[EvidenceSourceSchema] = []
    risk_scores: List[RiskScoreSchema] = []
    
    class Config:
        from_attributes = True

class VerificationHistoryItem(BaseModel):
    id: str
    status: str
    verdict: Optional[str]
    completed_at: Optional[datetime]
    claim: ClaimResponse
    confidence_score: Optional[int] = None
    
    class Config:
        from_attributes = True

class DailyStat(BaseModel):
    date: str
    analyzed: int
    false_claims: int
    hate_speech: int
    misleading: int

class PlatformStat(BaseModel):
    platform: str
    percentage: int

class DashboardStatsResponse(BaseModel):
    total_analyzed: int
    false_claims: int
    hate_speech: int
    verification_accuracy: int
    daily_stats: List[DailyStat]
    platform_stats: List[PlatformStat]
