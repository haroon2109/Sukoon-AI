from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import auth, verification
from app.api.v1.endpoints import verify

from app.db.session import engine
from app.domain.models.base import Base
from app.domain.models import claims, related_models, users, verifications

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sukoon", version="1.0.0", description="Verification Platform")

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the newly generated Phase 2 routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(verification.router, prefix="/api/v1", tags=["Verification"])

# Mount the verify endpoints for WebSockets and specific tasks
app.include_router(verify.router, prefix="/api/v1/verify", tags=["Verify"])

@app.get("/")
def root():
    return {"status": "Sukoon Core Running"}
