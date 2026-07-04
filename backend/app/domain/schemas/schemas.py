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

class RecommendedAction(str, Enum):
    FLAG = "FLAG"
    REMOVE = "REMOVE"
    MONITOR = "MONITOR"
    COUNTER_NARRATIVE = "COUNTER_NARRATIVE"
    NO_ACTION = "NO_ACTION"

class VerdictCategory(str, Enum):
    VERIFIED_TRUE = "VERIFIED_TRUE"
    FALSE = "FALSE"
    MISLEADING = "MISLEADING"
    UNVERIFIED_RUMOR = "UNVERIFIED_RUMOR"
    SATIRE = "SATIRE"
    TOXIC = "TOXIC"

class UserBase(BaseModel):
    email: EmailStr
    organization_name: Optional[str] = Field(None, max_length=100)
    
    @field_validator("organization_name")
    def sanitize_org_name(cls, v):
        if v is not None:
            # Strip null bytes and dangerous control characters
            cleaned = "".join(ch for ch in v if ord(ch) >= 32).strip()
            return bleach.clean(cleaned, strip=True)
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
    source_platform: SourcePlatform = SourcePlatform.OTHER

# --- Claim Schemas ---
class ClaimCreate(BaseModel):
    raw_content: str = Field(..., min_length=1, max_length=5000)
    language: Optional[str] = Field("en", max_length=10)
    
    @field_validator("raw_content")
    def sanitize_content(cls, v):
        if not v:
            raise ValueError("Content cannot be null or empty.")
        # Strip null bytes and non-printable control characters, preserving newlines
        cleaned = "".join(ch for ch in v if ord(ch) >= 32 or ch in "\n\r\t").strip()
        if not cleaned:
            raise ValueError("Content cannot consist only of whitespace or control characters.")
        return bleach.clean(cleaned, strip=True)

class ClaimResponse(BaseModel):
    id: str
    user_id: str
    raw_content: str
    extracted_claim: Optional[str]
    language: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ExtractedClaim(BaseModel):
    claim_text: str
    context: Optional[str] = None

class ExtractedClaimsList(BaseModel):
    claims: List[ExtractedClaim]

# --- Verification Schemas ---
class RetrievedEvidence(BaseModel):
    source_url: Optional[str]
    content: str
    relevance_score: Optional[float] = None

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

class Citation(BaseModel):
    source_url: str
    direct_quote: str
    justification: str

class FactVerificationOutput(BaseModel):
    summary_for_moderator: str
    verdict_category: VerdictCategory
    recommended_action: RecommendedAction
    confidence_score: float
    evidence_synthesis: str
    counter_narrative_suggestion: Optional[str] = None
    citations: List[Citation] = []

class VerificationResponse(BaseModel):
    id: str
    claim_id: str
    status: str
    verdict: Optional[str]
    explanation: Optional[str] = None
    generated_truth_card_url: Optional[str]
    evidence_sources: List[EvidenceSourceSchema] = []
    risk_scores: List[RiskScoreSchema] = []
    
    class Config:
        from_attributes = True

class ExplainableAIReport(BaseModel):
    id: str
    claim_id: str
    status: str
    summary_for_moderator: str
    verdict_category: VerdictCategory
    recommended_action: RecommendedAction
    confidence_score: float
    evidence_synthesis: str
    counter_narrative_suggestion: Optional[str] = None
    citations: List[Citation] = []
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
