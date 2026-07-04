from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.logger import api_logger, security_logger
from app.db.session import engine
from app.domain.models.base import Base

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Explicitly import all models so SQLAlchemy metadata registers their tables before create_all
    from app.domain.models import User, Claim, Verification, MediaAsset, EvidenceSource, RiskScore  # noqa: F401
    # Run database setup safely on startup
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Sukoon AI", version="1.0.0", description="Misinformation Verification Platform", lifespan=lifespan)

# ── Rate Limiter ──────────────────────────────────────────────────────────────
from slowapi.errors import RateLimitExceeded
from app.core.rate_limit import limiter, get_client_ip

def secure_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    security_logger.warning(
        "Rate limit exceeded",
        extra={"custom_data": {"client_ip": get_client_ip(request), "url": str(request.url)}}
    )
    return JSONResponse(status_code=429, content={"detail": "Too Many Requests. Please slow down."})

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, secure_rate_limit_handler)

# ── Exception Handlers ────────────────────────────────────────────────────────
from fastapi.exceptions import HTTPException

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    api_logger.error(
        "Unhandled API exception",
        exc_info=True,
        extra={"custom_data": {"client_ip": get_client_ip(request), "url": str(request.url)}}
    )
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})

# ── CORS ──────────────────────────────────────────────────────────────────────
from app.core.config import settings
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Celery default app configuration
from app.workers.celery_app import celery_app  # noqa: F401

# ── Routers ───────────────────────────────────────────────────────────────────
from app.api.v1.routers import auth, verification
from app.api.v1.endpoints import verify, n8n_webhooks, results

app.include_router(auth.router,          prefix="/api/v1/auth",   tags=["Authentication"])
app.include_router(verification.router,  prefix="/api/v1",        tags=["Verification"])
app.include_router(verify.router,        prefix="/api/v1/verify", tags=["Verify"])
app.include_router(results.router,       prefix="/api/v1",        tags=["Results"])
app.include_router(n8n_webhooks.router,  prefix="/api/v1/n8n",    tags=["n8n Automations"])

# ── Core Endpoints ────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "Sukoon AI is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    """Cloud Run health check — must return 200 for the service to stay alive."""
    return {"status": "healthy"}
