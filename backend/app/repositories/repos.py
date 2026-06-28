from sqlalchemy.orm import Session
from .base_repo import BaseRepository
from ..domain.models.users import User
from ..domain.models.claims import Claim
from ..domain.models.verifications import Verification
import uuid

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
        
    def get_by_email(self, db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    def get_by_api_key(self, db: Session, api_key: str) -> User:
        return db.query(User).filter(User.api_key == api_key).first()
        
    def create_user(self, db: Session, email: str, organization_name: str) -> User:
        # Generate a secure API key
        api_key = f"sk_live_{uuid.uuid4().hex}"
        return self.create(db, {
            "email": email,
            "organization_name": organization_name,
            "api_key": api_key
        })

class ClaimRepository(BaseRepository[Claim]):
    def __init__(self):
        super().__init__(Claim)

class VerificationRepository(BaseRepository[Verification]):
    def __init__(self):
        super().__init__(Verification)

user_repo = UserRepository()
claim_repo = ClaimRepository()
verification_repo = VerificationRepository()
