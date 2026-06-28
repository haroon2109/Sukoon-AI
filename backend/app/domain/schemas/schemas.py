from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    organization_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    api_key: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# --- Claim Schemas ---
class ClaimCreate(BaseModel):
    raw_content: str
    language: Optional[str] = "en"

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
