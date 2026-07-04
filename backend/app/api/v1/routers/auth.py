from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ....domain.schemas.schemas import UserCreate, UserResponse, UserLogin, Token
from ....services.auth_service import auth_service
from ....api.dependencies.database import get_db
from ....core.security import create_access_token
from jose import jwt, JWTError
from ....core.config import settings
from ....core.rate_limit import limiter

router = APIRouter()

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

@router.post("/register", response_model=UserResponse)
@limiter.limit("5/minute")
def register_organization(request: Request, user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user securely and sends a verification email.
    """
    return auth_service.create_organization(db, user_in)

@router.post("/login", response_model=Token)
@limiter.limit("10/minute")
def login(request: Request, user_login: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a JWT access token.
    """
    user = auth_service.authenticate_user(db, user_login)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified. Check your inbox or use /auth/resend-verification.")
        
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    """
    Verifies a user's email using the JWT token sent via email.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        if email is None or token_type != "verification":
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token")
        
    auth_service.verify_email(db, email=email)
    return {"message": "Email verified successfully. You may now log in."}

@router.post("/forgot-password")
@limiter.limit("3/minute")
def forgot_password(request: Request, email: str, db: Session = Depends(get_db)):
    """
    Generates a password reset token and sends it via email.
    """
    auth_service.create_password_reset_token(db, email)
    return {"message": "If that email is registered, a password reset link has been sent."}

@router.post("/reset-password")
@limiter.limit("3/minute")
def reset_password(request: Request, data: PasswordResetConfirm, db: Session = Depends(get_db)):
    """
    Resets the user's password using the provided token.
    """
    auth_service.reset_password(db, data.token, data.new_password)
    return {"message": "Password has been successfully reset."}
