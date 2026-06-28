from sqlalchemy.orm import Session
from ..repositories.repos import claim_repo, verification_repo
from ..domain.schemas.schemas import ClaimCreate
import uuid

class VerificationService:
    def ingest_payload(self, db: Session, claim_in: ClaimCreate, user_id: str):
        # 1. Save Raw Claim
        new_claim = claim_repo.create(db, {
            "user_id": user_id,
            "raw_content": claim_in.raw_content,
            "language": claim_in.language
        })
        
        # 2. Create Pending Verification Record
        new_verification = verification_repo.create(db, {
            "claim_id": new_claim.id,
            "user_id": user_id,
            "status": "pending"
        })
        
        # 3. Synchronous verification for MVP removed - handled by WebSocket
        return new_verification

verification_service = VerificationService()
