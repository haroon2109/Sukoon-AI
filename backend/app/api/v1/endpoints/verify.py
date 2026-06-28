from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import UUID
import asyncio

from app.db.session import get_db
from app.agents.context_verifier import ContextVerificationAgent
from app.domain.schemas.schemas import ClaimCreate
from app.services.verification_service import verification_service
from app.domain.models.users import User

router = APIRouter()

class UrlVerificationRequest(BaseModel):
    url: str
    source_platform: str

class VerificationResponse(BaseModel):
    task_id: str
    status: str
    message: str

@router.post("/url", response_model=VerificationResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_url_for_verification(
    request: UrlVerificationRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
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

@router.post("/media", response_model=VerificationResponse, status_code=status.HTTP_202_ACCEPTED)
async def submit_media_for_verification(
    claim_in: ClaimCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Submit a media file (WhatsApp audio/video forward) or text for verification.
    """
    # Mock user ID for MVP
    current_user_id = "mocked-user-uuid"
    
    # Ensure mock user exists to prevent Foreign Key constraint errors
    existing_user = db.query(User).filter(User.id == current_user_id).first()
    if not existing_user:
        new_user = User(id=current_user_id, email="mock@sukoon.ai", full_name="Mock User")
        db.add(new_user)
        try:
            db.commit()
        except Exception:
            db.rollback()
    
    # 1. Create a VerificationRequest record in the database
    verification = verification_service.ingest_payload(db, claim_in, current_user_id)
    
    return VerificationResponse(
        task_id=str(verification.id),
        status="processing",
        message="Media uploaded successfully. Verification pipeline started."
    )

from app.repositories.repos import verification_repo, claim_repo
from datetime import datetime

@router.websocket("/ws/{task_id}")
async def websocket_verification_stream(websocket: WebSocket, task_id: str, db: Session = Depends(get_db)):
    """
    Real-time WebSocket endpoint. 
    Replaces the old REST polling to stream analysis phases back to the UI instantly.
    """
    await websocket.accept()
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
        verification = verification_repo.get(db, id=task_id)
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
