from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ....domain.schemas.schemas import UserCreate, UserResponse
from ....services.auth_service import auth_service
from ....api.dependencies.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_organization(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new B2B client and returns an API Key.
    """
    return auth_service.create_organization(db, user_in)
