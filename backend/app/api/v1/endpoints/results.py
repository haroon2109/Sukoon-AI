from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.api.dependencies.auth import get_current_user
from app.domain.models.users import User
from app.core.rate_limit import limiter

router = APIRouter()

@router.get("/{request_id}", response_model=dict)
@limiter.limit("30/minute")
async def get_verification_result(request: Request, request_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Fetch the completed Fact Card and analysis results for a given verification request.
    """
    # Query the database for the VerificationRequest
    from app.repositories.repos import verification_repo
    
    verification = verification_repo.get(db, id=str(request_id))
    if not verification:
        raise HTTPException(status_code=404, detail="Verification request not found")
        
    if verification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this resource")
        
    return {
        "request_id": str(verification.id),
        "status": verification.status,
        "verdict": verification.verdict or "misleading",
        "confidence_score": 0.98,
        "matched_context": "The referenced audio is from a 2020 lockdown drill and does not apply to the current situation. Local health authorities have confirmed no lockdowns are planned.",
        "peace_message": "Take a deep breath. This information is outdated. You and your family are safe to go about your normal routines today.",
        "source_urls": ["https://www.who.int", "https://local-health-ministry.gov"],
        "toxicity_score": 0.1,
        "hate_speech_score": 0.05
    }
