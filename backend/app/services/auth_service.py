from sqlalchemy.orm import Session
from ..repositories.repos import user_repo
from ..domain.schemas.schemas import UserCreate, UserLogin
from ..core.security import get_password_hash, verify_password, create_verification_token
from fastapi import HTTPException
import uuid
from ..core.logger import security_logger

class AuthService:
    def create_organization(self, db: Session, user_in: UserCreate):
        existing_user = user_repo.get_by_email(db, user_in.email)
        if existing_user:
            security_logger.warning("Registration failed: Email already exists", extra={"custom_data": {"email": user_in.email}})
            raise HTTPException(status_code=400, detail="Email already registered")
        
        hashed_pw = get_password_hash(user_in.password)
        verification_token = create_verification_token(user_in.email)
        
        # We still generate an api_key for backend usage, but use JWT for frontend
        api_key = str(uuid.uuid4())
        
        user = user_repo.create_user(
            db, 
            email=user_in.email, 
            organization_name=user_in.organization_name,
            hashed_password=hashed_pw,
            api_key=api_key,
            verification_token=verification_token
        )
        
        security_logger.info("New user registered", extra={"custom_data": {"email": user.email, "user_id": user.id}})
        
        from ..core.config import settings
        if settings.ENVIRONMENT == "development":
            # Auto-verify in development so new users can immediately log in
            user.is_verified = True
            db.commit()
            security_logger.info("Auto-verified user in development mode", extra={"custom_data": {"email": user.email}})
        else:
            # Production: send real verification email
            # TODO: Replace with SendGrid/Resend call
            print(f"MOCK EMAIL: Verify your email: /api/v1/auth/verify-email?token={verification_token}")
        
        return user
        
    def authenticate_user(self, db: Session, user_login: UserLogin):
        user = user_repo.get_by_email(db, user_login.email)
        if not user:
            security_logger.warning("Failed login attempt: User not found", extra={"custom_data": {"email": user_login.email}})
            return False
        if not verify_password(user_login.password, user.hashed_password):
            security_logger.warning("Failed login attempt: Incorrect password", extra={"custom_data": {"email": user_login.email}})
            return False
        security_logger.info("Successful login", extra={"custom_data": {"email": user.email, "user_id": user.id}})
        return user
        
    def verify_email(self, db: Session, email: str):
        user = user_repo.get_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.is_verified:
            raise HTTPException(status_code=400, detail="Email already verified")
            
        user.is_verified = True
        user.verification_token = None
        db.commit()
        return user
    
    def create_password_reset_token(self, db: Session, email: str):
        user = user_repo.get_by_email(db, email)
        if not user:
            # Don't reveal if user exists or not
            return None
            
        from datetime import datetime, timedelta
        from jose import jwt
        from ..core.config import settings
        
        expire = datetime.utcnow() + timedelta(hours=1)
        to_encode = {"sub": email, "type": "password_reset", "exp": expire}
        token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        # Mock sending email
        security_logger.info("Password reset requested", extra={"custom_data": {"email": email}})
        print(f"MOCK EMAIL: Reset your password by clicking: /api/v1/auth/reset-password?token={token}")
        return token
        
    def reset_password(self, db: Session, token: str, new_password: str):
        from jose import jwt, JWTError
        from ..core.config import settings
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            token_type: str = payload.get("type")
            if email is None or token_type != "password_reset":
                raise HTTPException(status_code=400, detail="Invalid token")
        except JWTError:
            security_logger.warning("Failed password reset: Invalid token used")
            raise HTTPException(status_code=400, detail="Invalid token")
            
        user = user_repo.get_by_email(db, email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        hashed_pw = get_password_hash(new_password)
        user.hashed_password = hashed_pw
        db.commit()
        
        security_logger.info("Password successfully reset", extra={"custom_data": {"email": email, "user_id": user.id}})
        return True

    def validate_api_key(self, db: Session, api_key: str):
        user = user_repo.get_by_api_key(db, api_key)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid API Key")
        return user

auth_service = AuthService()
