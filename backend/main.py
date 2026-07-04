from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.logger import api_logger, security_logger
from app.db.session import engine
from app.domain.models.base import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sukoon", version="1.0.0", description="Verification Platform")

# Rate Limiter Configuration
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter

def secure_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    security_logger.warning("Rate limit exceeded", extra={"custom_data": {"client_ip": request.client.host, "url": str(request.url)}})
    return JSONResponse(status_code=429, content={"detail": "Too Many Requests"})

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, secure_rate_limit_handler)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    api_logger.error("Unhandled API exception", exc_info=True, extra={"custom_data": {"client_ip": request.client.host, "url": str(request.url)}})
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
from app.api.v1.routers import auth, verification
from app.api.v1.endpoints import verify, n8n_webhooks
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(verification.router, prefix="/api/v1", tags=["Verification"])
app.include_router(verify.router, prefix="/api/v1/verify", tags=["Verify"])
app.include_router(n8n_webhooks.router, prefix="/api/v1/n8n", tags=["n8n Automations"])

@app.get("/")
def root():
    return {"status": "Sukoon Core Running"}

