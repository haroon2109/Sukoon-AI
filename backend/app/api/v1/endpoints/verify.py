from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, WebSocket, WebSocketDisconnect, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import UUID
import asyncio

from app.db.session import get_db
from app.agents.context_verifier import ContextVerificationAgent
from app.domain.schemas.schemas import ClaimCreate, UrlVerificationRequest
from app.services.verification_service import verification_service
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
    """
    Submit a URL (e.g., from X or Instagram) for verification.
    This endpoint creates a database record and triggers the Celery pipeline.
    """
    # 1. Create a VerificationRequest record in the database using db session
    # 2. Trigger Celery fan-out pipeline (ClaimExtraction, HateSpeech, VisualVerify)
    
    # Mocking the response for MVP
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
    """
    Submit a media file (audio/video/image) for verification securely.
    """
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, MP3, and MP4 are allowed.")
        
    safe_filename = secure_filename(file.filename)
    
    # Check size by reading in chunks to avoid memory issues and stop early
    file_size = 0
    while chunk := await file.read(8192):
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
            
    # Reset file pointer for future processing
    await file.seek(0)
    
    # In a real app, save to GCP Cloud Storage here using safe_filename
    
    # Create a mock ClaimCreate to satisfy the current ingest_payload signature
    claim_in = ClaimCreate(raw_content=f"Uploaded media: {safe_filename}")
    
    # 1. Create a VerificationRequest record in the database
    verification = verification_service.ingest_payload(db, claim_in, current_user.id)
    
    return VerificationResponse(
        task_id=str(verification.id),
        status="processing",
        message="Media uploaded successfully. Verification pipeline started."
    )

from app.repositories.repos import verification_repo, claim_repo
from datetime import datetime

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
    
    # Manually authenticate via token query parameter
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
        
    # Enforce IDOR ownership check
    verification = verification_repo.get(db, id=task_id)
    if not verification:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Verification not found")
        return
        
    if verification.user_id != current_user.id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Not authorized")
        return

    try:
        # Mock streaming the agent pipeline execution (progress events)
        stages = [
            {"step": "ingestion", "message": "Parsing media payload..."},
            {"step": "extraction", "message": "Extracting claims via LLM..."},
            {"step": "vector_search", "message": "Querying Qdrant for known facts..."},
            {"step": "synthesis", "message": "Synthesizing Peace Message..."}
        ]
        
        for stage in stages:
            await asyncio.sleep(1.0)  # Simulate processing delay
            await websocket.send_json(stage)
            
        # 1. Fetch Verification and Claim from DB
        # Verification already fetched above for IDOR check
        claim_text = "Unknown claim"
        if verification and verification.claim_id:
            claim = claim_repo.get(db, id=verification.claim_id)
            if claim:
                claim_text = claim.raw_content
                
        # 2. Run actual agent logic on the REAL claim
        from app.ai_modules.agents.evaluation_agent import evaluation_agent
        result = await asyncio.to_thread(evaluation_agent.evaluate, claim_text)
        
        # 3. Update Verification record in DB
        raw_verdict = result.get("verdict", "Safe").lower()
        if "safe" in raw_verdict:
            frontend_verdict = "verified"
        elif "misleading" in raw_verdict:
            frontend_verdict = "misleading"
        else:
            frontend_verdict = "false"
            
        if verification:
            verification_repo.update(db, db_obj=verification, obj_in={
                "status": "completed",
                "verdict": frontend_verdict,
                "completed_at": datetime.utcnow()
            })
        
        # 4. Send completed payload
        completed_stage = {
            "step": "completed", 
            "message": "Verification complete. Generating Truth Card.",
            "data": {
                "verdict": frontend_verdict,
                "confidenceScore": int(result.get("confidence_score", 0.9) * 100),
                "claimSummary": claim_text[:100] + "...",
                "actualFacts": result.get("explanation", ""),
                "sourceCitations": result.get("sourceCitations", []),
                "peaceMessage": result.get("suggested_action", "Your community relies on facts. Thank you for verifying before sharing."),
                "toxicityScore": result.get("toxicity_score", 0),
                "factualityScore": result.get("factuality_score", 100)
            }
        }
        await asyncio.sleep(0.5)
        await websocket.send_json(completed_stage)
        await websocket.close()
            
    except WebSocketDisconnect:
        print(f"Client disconnected from task: {task_id}")
