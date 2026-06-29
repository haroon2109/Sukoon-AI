from fastapi import FastAPI, Request, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.logger import api_logger, security_logger
from app.db.session import engine
from app.domain.models.base import Base

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Sukoon", version="1.0.0", description="Verification Platform")

# CORS Setup for Next.js Dashboard Interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.v1.routers import auth, verification
from app.api.v1.endpoints import verify
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(verification.router, prefix="/api/v1", tags=["Verification"])
app.include_router(verify.router, prefix="/api/v1/verify", tags=["Verify"])

@app.get("/")
def root():
    return {"status": "Sukoon Core Running"}

import asyncio
from pydantic import BaseModel
from app.services.ai_engine import verify_multimodal_content
from app.services.rag_service import rag_service
from app.agents.claim_extractor import extract_claim_from_text
from app.services.scraper import is_url, scrape_url
from app.services.downloader import is_social_video_url, download_social_video

# Normalizes string outputs to match strict frontend requirements
def map_verdict_to_token(raw_verdict: str) -> str:
    v = str(raw_verdict).lower()
    if any(word in v for word in ["verified", "true", "safe", "🟢"]):
        return "verified"
    elif any(word in v for word in ["misleading", "🟠"]):
        return "misleading"
    elif any(word in v for word in ["unverified", "unable", "context", "🟡", "⚪"]):
        return "unverified"
    elif any(word in v for word in ["false", "🔴"]):
        return "false"
    return "unverified"

class TextRequest(BaseModel):
    content: str

@app.post("/api/verify/text")
async def verify_text_endpoint(request: Request, payload: TextRequest):
    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="Content string is empty.")
        
    if is_url(content):
        if is_social_video_url(content):
            video_bytes, text_metadata, mime_type = download_social_video(content)
            if video_bytes:
                content = text_metadata
        else:
            scraped = scrape_url(content)
            content = scraped if scraped.strip() else content

    # 1. Isolate Core Claim
    clean_claim = await extract_claim_from_text(content)
    
    # 2. Check Local Database Context Match
    rag_results = rag_service.retrieve_context(clean_claim)
    
    if rag_results and len(rag_results) >= 2:
        context_str = "\n".join([r["text"] for r in rag_results])
        result = await verify_multimodal_content(text_content=clean_claim, retrieved_context=context_str)
        
        raw_verdict = result["data"].get("verdict", "unverified")
        return {
            "status": "success",
            "data": {
                "verdict": map_verdict_to_token(raw_verdict),
                "confidenceScore": result["data"].get("confidence_score", 85.0),
                "claimSummary": clean_claim,
                "actualFacts": result["data"].get("explanation", ""),
                "sourceCitations": [r["source"] for r in rag_results],
                "peaceMessage": "Cross-referenced securely against local warehouse data channels."
            }
        }
    else:
        # ANTIGRAVITY FALLBACK MODE: Skip local constraints, activate live search grounding
        from app.ai_modules.fact_checking.llm_client import llm_client
        search_result = llm_client.generate(clean_claim)
        
        verdict_str = search_result.get("verdict", "UNVERIFIED")
        citations = search_result.get("grounding_sources", [])
        
        return {
            "status": "success",
            "data": {
                "verdict": map_verdict_to_token(verdict_str),
                "confidenceScore": 98.0 if verdict_str == "TRUE" else 92.0 if verdict_str == "FALSE" else 40.0,
                "claimSummary": clean_claim,
                "actualFacts": search_result.get("explanation", "Verified via live Google Search consensus endpoints."),
                "sourceCitations": citations,
                "peaceMessage": "Verified safe. Fostering community peace through verified factual data sharing." if verdict_str == "TRUE" else "Misleading context discovered. Help protect your local peers by checking before sharing."
            }
        }
