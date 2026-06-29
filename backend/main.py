from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.api.v1.routers import auth, verification
from app.api.v1.endpoints import verify
from fastapi.responses import JSONResponse
from app.core.logger import api_logger, security_logger

from app.db.session import engine
from app.domain.models.base import Base
from app.domain.models import claims, related_models, users, verifications

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sukoon", version="1.0.0", description="Verification Platform")

# Enforce HTTPS
# Uncomment in true production if Cloud Run isn't terminating SSL fully, or if you want strict app-level enforcement
# app.add_middleware(HTTPSRedirectMiddleware)

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

# --- Antigravity Agent Verification ---
import asyncio
from pydantic import BaseModel
from fastapi import HTTPException
from app.services.ai_engine import verify_multimodal_content

async def run_sukoon_agent(user_query: str):
    # Configure the agent to run securely within your Google Cloud project bounds
    import os
    config = LocalAgentConfig(
        api_key=os.getenv("GEMINI_API_KEY"),
        system_instructions=(
            "You are an autonomous Sukoon AI agent. Your mission is to investigate the provided text "
            "or link for community hatred or fake news. You have access to Google Search and URL web context "
            "to independently verify facts before providing a final peace verdict."
        )
    )
    
    # Initialize the runtime (automatically hooks up web search and isolated tool usage loops)
    async with Agent(config) as agent:
        response = await agent.chat(f"Investigate this claim: {user_query}")
        return await response.text()

class TextRequest(BaseModel):
    content: str

# Pipeline 1 & 2: Handles Raw Text & Pasted Article Links
@app.post("/api/verify/text")
@limiter.limit("10/minute")
async def verify_text_endpoint(request: Request, payload: TextRequest):
    if not payload.content.strip():
        raise HTTPException(status_code=400, detail="Content string is empty.")
    
    # If it's a link, we pass the URL string directly. 
    # Gemini handles browsing context automatically if given the URL in a grounded prompt.
    result = await verify_multimodal_content(text_content=payload.content)
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result

# Pipeline 3: Handles Uploaded Images / Videos
@app.post("/api/verify/media")
@limiter.limit("5/minute")
async def verify_media_endpoint(
    request: Request,
    content: str = Form(None), # Optional accompanying text text description
    file: UploadFile = File(...)
):
    # Validate accepted media types for safety boundaries
    allowed_types = ["image/jpeg", "image/png", "image/webp", "video/mp4"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
        
    # Read raw bytes straight out of the multi-part request stream
    file_bytes = await file.read()
    
    result = await verify_multimodal_content(
        text_content=content,
        media_bytes=file_bytes,
        mime_type=file.content_type
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    return result
