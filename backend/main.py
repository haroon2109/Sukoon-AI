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
from app.services.rag_service import rag_service
from app.agents.claim_extractor import extract_claim_from_text
from app.services.scraper import is_url, scrape_url
from app.services.downloader import is_social_video_url, download_social_video

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

from datetime import datetime

def calculate_dynamic_confidence(rag_results: list, llm_raw_confidence: float) -> float:
    if not rag_results:
        return min(llm_raw_confidence, 50.0)
        
    best_doc = rag_results[0]
    
    # 1. Evidence Similarity (40%)
    sim = best_doc.get("similarity", 0.0)
    sim_score = min(max(sim * 40.0, 0.0), 40.0)
    
    # 2. Source Reliability (30%)
    source = best_doc.get("source", "").lower()
    source_score = 15.0 # Default 50% of max
    if "who" in source or "imd" in source or "government" in source:
        source_score = 30.0
    elif "pib" in source or "alt news" in source:
        source_score = 27.0
    elif "boom" in source:
        source_score = 25.5
        
    # 3. LLM Consistency (20%)
    llm_score = min(max((llm_raw_confidence / 100.0) * 20.0, 0.0), 20.0)
    
    # 4. Metadata Freshness (10%)
    freshness_score = 5.0
    date_str = best_doc.get("date", "")
    if date_str:
        try:
            doc_date = datetime.strptime(date_str, "%Y-%m-%d")
            days_old = (datetime.now() - doc_date).days
            if days_old < 365:
                freshness_score = 10.0
            elif days_old < 365 * 3:
                freshness_score = 7.0
            else:
                freshness_score = 3.0
        except ValueError:
            pass
            
    total = sim_score + source_score + llm_score + freshness_score
    return round(min(max(total, 0.0), 100.0), 2)

class TextRequest(BaseModel):
    content: str

# Pipeline 1 & 2: Handles Raw Text & Pasted Article Links
@app.post("/api/verify/text")
@limiter.limit("10/minute")
async def verify_text_endpoint(request: Request, payload: TextRequest):
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Content string is empty.")
        
    # Check if input is a URL
    if is_url(content):
        if is_social_video_url(content):
            video_bytes, text_metadata, mime_type = download_social_video(content)
            if video_bytes:
                # If we successfully downloaded a video, process it with the multimodal flow
                clean_claim = await extract_claim_from_text(text_metadata)
                
                context_str = "NO EVIDENCE FOUND IN KNOWLEDGE BASE."
                rag_results = []
                if clean_claim:
                    rag_results = rag_service.retrieve_context(clean_claim)
                    if rag_results:
                        context_str = "\n".join([r["text"] for r in rag_results])
                
                result = await verify_multimodal_content(
                    text_content=clean_claim,
                    media_bytes=video_bytes,
                    mime_type=mime_type,
                    retrieved_context=context_str
                )
                
                if result["status"] == "error":
                    raise HTTPException(status_code=500, detail=result["message"])
                    
                raw_conf = result["data"].get("confidence_score", 50.0)
                dynamic_conf = calculate_dynamic_confidence(rag_results, raw_conf)
                
                if len(rag_results) < 2:
                    result["data"]["verdict"] = "⚪ Unable to Verify"
                    dynamic_conf = 0.0
                    result["data"]["explanation"] = "Insufficient evidence to confidently verify this claim. Minimum 2 trusted sources required. " + result["data"].get("explanation", "")
                
                result["data"]["confidence_score"] = dynamic_conf
                result["data"]["claimSummary"] = clean_claim
                result["data"]["evidenceFound"] = "\n\n".join([r["text"] for r in rag_results]) if rag_results else "No verified evidence matched in database."
                result["data"]["aiExplanation"] = result["data"].get("explanation", "")
                result["data"]["sourceCitations"] = [r["source"] for r in rag_results] if rag_results else []
                
                return result
                
        # If not a social video, or download failed, try normal web scraping
        scraped_text = scrape_url(content)
        if not scraped_text.strip():
            # Fallback logic: If content is blocked behind a bot-protection firewall,
            # pass the raw URL alongside a direct request for Gemini to look it up via Search Grounding instead.
            content = f"Please research this specific URL link directly using your live search tool: {content}"
        else:
            # Provide the scraped text to the pipeline
            content = f"Article Content: {scraped_text[:5000]}"
    
    # 1. Claim Extraction
    clean_claim = await extract_claim_from_text(content)
    
    # 2. Retrieve local RAG context using clean claim
    rag_results = rag_service.retrieve_context(clean_claim)
    if rag_results:
        context_str = "\n".join([r["text"] for r in rag_results])
        citations = [r["source"] for r in rag_results]
    else:
        context_str = "NO EVIDENCE FOUND IN KNOWLEDGE BASE."
        citations = []
    
    # 3. Final Verification (pass the clean claim to reduce reasoning noise)
    result = await verify_multimodal_content(text_content=clean_claim, retrieved_context=context_str)
    
    if result["status"] == "error":
        error_str = result["message"]
        if "429" in error_str or "Quota" in error_str:
            raise HTTPException(
                status_code=429, 
                detail="Sukoon AI is experiencing heavy viral traffic. Please wait a moment and try verifying again."
            )
        raise HTTPException(status_code=500, detail=error_str)
        
    # Combine signals for the dynamic confidence score
    raw_conf = result["data"].get("confidence_score", 50.0)
    dynamic_conf = calculate_dynamic_confidence(rag_results if 'rag_results' in locals() and rag_results else [], raw_conf)
    
    # GUARDRAIL: Require minimum 2 pieces of evidence
    if len(rag_results) < 2:
        result["data"]["verdict"] = "⚪ Unable to Verify"
        dynamic_conf = 0.0
        result["data"]["explanation"] = "Insufficient evidence to confidently verify this claim. Minimum 2 trusted sources required. " + result["data"].get("explanation", "")
        
    result["data"]["confidence_score"] = dynamic_conf
    result["data"]["claimSummary"] = clean_claim
    result["data"]["evidenceFound"] = context_str
    result["data"]["aiExplanation"] = result["data"].get("explanation", "")
    result["data"]["sourceCitations"] = citations
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
    allowed_types = [
        "image/jpeg", "image/png", "image/webp", 
        "video/mp4",
        "audio/ogg", "audio/mp3", "audio/mpeg", "audio/wav", "audio/m4a"
    ]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.content_type}")
        
    # Read raw bytes straight out of the multi-part request stream
    file_bytes = await file.read()
    
    # 1. Extract claim from text if provided (Media handles OCR implicitly in Gemini)
    clean_claim = ""
    if content:
        clean_claim = await extract_claim_from_text(content)
        
    # 2. Retrieve local RAG context
    context_str = "NO EVIDENCE FOUND IN KNOWLEDGE BASE."
    citations = []
    if clean_claim:
        rag_results = rag_service.retrieve_context(clean_claim)
        if rag_results:
            context_str = "\n".join([r["text"] for r in rag_results])
            citations = [r["source"] for r in rag_results]
    
    # 3. Final Verification
    result = await verify_multimodal_content(
        text_content=clean_claim,
        media_bytes=file_bytes,
        mime_type=file.content_type,
        retrieved_context=context_str
    )
    
    if result["status"] == "error":
        error_str = result["message"]
        if "429" in error_str or "Quota" in error_str:
            raise HTTPException(
                status_code=429, 
                detail="Sukoon AI is experiencing heavy viral traffic. Please wait a moment and try verifying again."
            )
        raise HTTPException(status_code=500, detail=error_str)
        
    # Combine signals for the dynamic confidence score
    raw_conf = result["data"].get("confidence_score", 50.0)
    
    rag_list = rag_results if 'rag_results' in locals() and rag_results else []
    dynamic_conf = calculate_dynamic_confidence(rag_list, raw_conf)
        
    # GUARDRAIL: Require minimum 2 pieces of evidence
    if len(rag_list) < 2:
        result["data"]["verdict"] = "⚪ Unable to Verify"
        dynamic_conf = 0.0
        result["data"]["explanation"] = "Insufficient evidence to confidently verify this claim. Minimum 2 trusted sources required. " + result["data"].get("explanation", "")
        
    result["data"]["confidence_score"] = dynamic_conf
    result["data"]["claimSummary"] = clean_claim
    result["data"]["evidenceFound"] = context_str
    result["data"]["aiExplanation"] = result["data"].get("explanation", "")
    result["data"]["sourceCitations"] = citations
    return result
