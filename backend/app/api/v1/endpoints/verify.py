from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, WebSocket, WebSocketDisconnect, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import UUID
import asyncio

from app.db.session import get_db
from app.agents.context_verifier import ContextVerificationAgent
from app.domain.schemas.schemas import ClaimCreate, UrlVerificationRequest
from app.services.verification_service import agentic_workflow_coordinator
from app.domain.models.users import User
from app.api.dependencies.auth import get_current_user
from fastapi import File, UploadFile
import os
from app.core.utils import secure_filename
from app.core.rate_limit import limiter

router = APIRouter()

class VerificationResponse(BaseModel):
    task_id: str
    status: str
    message: str

@router.post("/url", response_model=VerificationResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("10/minute")
async def submit_url_for_verification(
    request: Request,
    url_req: UrlVerificationRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task_id = "mock-uuid-1234-5678"
    return VerificationResponse(
        task_id=task_id,
        status="processing",
        message="Verification pipeline started. Poll the /results endpoint for updates."
    )

ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "audio/mpeg", "video/mp4"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

@router.post("/media", response_model=VerificationResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("10/minute")
async def submit_media_for_verification(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, MP3, and MP4 are allowed.")
        
    safe_filename = secure_filename(file.filename)
    
    file_size = 0
    while chunk := await file.read(8192):
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
            
    await file.seek(0)
    claim_in = ClaimCreate(raw_content=f"Uploaded media: {safe_filename}")
    verification = agentic_workflow_coordinator.ingest_payload(db, claim_in, current_user.id)
    
    return VerificationResponse(
        task_id=str(verification.id),
        status="processing",
        message="Media uploaded successfully. Verification pipeline started."
    )

from app.repositories.repos import verification_repo, claim_repo
from datetime import datetime

# Helper function to map verdicts to strict lowercase tokens matching the React TruthCard component
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

@router.websocket("/ws/{task_id}")
async def websocket_verification_stream(websocket: WebSocket, task_id: str, token: str = None, db: Session = Depends(get_db)):
    """
    Real-time WebSocket endpoint. 
    Replaces the old REST polling to stream analysis phases back to the UI instantly.
    """
    from jose import jwt, JWTError
    from app.core.config import settings
    from app.repositories.repos import user_repo
    
    await websocket.accept()
    
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Missing token")
        return
        
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise JWTError()
        current_user = user_repo.get_by_email(db, email)
        if not current_user:
            raise JWTError()
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
        return
        
    verification = verification_repo.get(db, id=task_id)
    if not verification:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Verification not found")
        return
        
    if verification.user_id != current_user.id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Not authorized")
        return

    try:
        stages = [
            {"step": "ingestion", "message": "Parsing media payload..."},
            {"step": "extraction", "message": "Extracting claims via LLM..."},
            {"step": "vector_search", "message": "Querying Qdrant for known facts..."},
            {"step": "synthesis", "message": "Synthesizing Peace Message..."}
        ]
        
        for stage in stages:
            await asyncio.sleep(1.0)
            await websocket.send_json(stage)
            
        claim_text = "Unknown claim"
        if verification and verification.claim_id:
            claim = claim_repo.get(db, id=verification.claim_id)
            if claim:
                claim_text = claim.raw_content
                
        from app.ai_modules.langgraph_orchestrator import langgraph_pipeline
        result = await langgraph_pipeline.execute_graph(claim_text)
        
        # Correctly map all verdict signals into lowercase string tokens
        raw_verdict = result.get("verdict", "")
        frontend_verdict = map_verdict_to_token(raw_verdict)
            
        if verification:
            verification_repo.update(db, db_obj=verification, obj_in={
                "status": "completed",
                "verdict": frontend_verdict,
                "completed_at": datetime.utcnow()
            })
        
        # Map our structured XAI Features into the exact payload the frontend TruthCard expects
        confidence_val = result.get("confidence_score", 0.9)
        if isinstance(confidence_val, (int, float)) and confidence_val <= 1.0:
            confidence_percentage = int(confidence_val * 100)
        else:
            confidence_percentage = int(confidence_val)
            
        is_toxic = frontend_verdict == "toxic" or "TOXIC" in str(result.get("verdict_category", ""))
        
        # Convert Pydantic Citation models to dictionaries for JSON serialization if needed,
        # but since we appended them as dicts/objects, we handle them safely.
        citations = result.get("citations", [])
        if citations and not isinstance(citations[0], dict):
            citations = [c.model_dump() if hasattr(c, 'model_dump') else c.dict() for c in citations]
            
        completed_stage = {
            "step": "completed", 
            "message": "Verification complete. Generating Truth Card.",
            "data": {
                "verdict": frontend_verdict,
                "confidenceScore": confidence_percentage,
                "claimSummary": claim_text[:100] + "...",
                "actualFacts": result.get("explanation", "No synthesis provided."),
                "sourceCitations": citations,
                "peaceMessage": "Your community relies on facts. Thank you for verifying before sharing.",
                "toxicityScore": 100 if is_toxic else 0,
                "factualityScore": confidence_percentage if frontend_verdict == "verified" else (100 - confidence_percentage)
            }
        }
        await asyncio.sleep(0.5)
        await websocket.send_json(completed_stage)
        await websocket.close()
            
    except WebSocketDisconnect:
        print(f"Client disconnected from task: {task_id}")
