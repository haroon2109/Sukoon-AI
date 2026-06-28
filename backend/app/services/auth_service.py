from sqlalchemy.orm import Session
from ..repositories.repos import user_repo
from ..domain.schemas.schemas import UserCreate
from fastapi import HTTPException

class AuthService:
    def create_organization(self, db: Session, user_in: UserCreate):
        existing_user = user_repo.get_by_email(db, user_in.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        return user_repo.create_user(db, email=user_in.email, organization_name=user_in.organization_name)
    
    def validate_api_key(self, db: Session, api_key: str):
        user = user_repo.get_by_api_key(db, api_key)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid API Key")
        return user

auth_service = AuthService()
