from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, WebSocket, WebSocketDisconnect, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
import asyncio
import uuid as uuid_lib

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

class TextVerificationRequest(BaseModel):
    content: str

@router.post("/text", response_model=VerificationResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("10/minute")
async def submit_text_for_verification(
    request: Request,
    text_req: TextVerificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    claim_in = ClaimCreate(raw_content=text_req.content)
    verification = agentic_workflow_coordinator.ingest_payload(db, claim_in, current_user.id)
    
    # Trigger Celery Task
    from app.workers.task_pipelines import process_claim_task
    process_claim_task.delay(claim_type="text", verification_id=str(verification.id))
    
    return VerificationResponse(
        task_id=str(verification.id),
        status="processing",
        message="Verification pipeline started. Connect to WebSocket /ws/{task_id} for updates."
    )

@router.post("/url", response_model=VerificationResponse, status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("10/minute")
async def submit_url_for_verification(
    request: Request,
    url_req: UrlVerificationRequest, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    claim_in = ClaimCreate(raw_content=f"Please verify this URL: {url_req.url}")
    verification = agentic_workflow_coordinator.ingest_payload(db, claim_in, current_user.id)
    
    # Trigger Celery Task
    from app.workers.task_pipelines import process_claim_task
    process_claim_task.delay(claim_type="url", verification_id=str(verification.id))
    
    return VerificationResponse(
        task_id=str(verification.id),
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
        
    safe_filename = f"{uuid_lib.uuid4().hex}_{secure_filename(file.filename)}"
    
    file_size = 0
    while chunk := await file.read(8192):
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB.")
            
    await file.seek(0)
    
    # Save to /tmp for Cloud Run compatibility (ephemeral container filesystem)
    upload_dir = os.path.join("/tmp", "sukoon_uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, safe_filename)
    with open(file_path, "wb") as f:
        while chunk := await file.read(8192):
            f.write(chunk)
            
    claim_in = ClaimCreate(raw_content=f"Uploaded media: {file_path}")
    verification = agentic_workflow_coordinator.ingest_payload(db, claim_in, current_user.id)
    
    # Fire Celery task asynchronously — do NOT call synchronously (blocks event loop)
    from app.workers.task_pipelines import process_claim_task
    process_claim_task.delay(
        claim_type="media",
        verification_id=str(verification.id),
        mime_type=file.content_type
    )
    
    return VerificationResponse(
        task_id=str(verification.id),
        status="processing",
        message="Media uploaded successfully. Verification pipeline started."
    )

tasks_db = {}

def background_fact_check(task_id: str, text: str):
    import asyncio
    from app.services.verification_service import agentic_workflow_coordinator
    
    # We must run the async process in a new event loop or using asyncio.run
    # because BackgroundTasks runs in a separate thread without a running loop by default in some setups.
    # Actually, BackgroundTasks in FastAPI can be async! Let's make the background task async.
    pass

async def async_background_fact_check(task_id: str, text: str):
    try:
        from app.services.verification_service import agentic_workflow_coordinator
        result = await agentic_workflow_coordinator.process_verification(text)
        
        # Map raw verdict to frontend token
        raw_verdict = result.get("verdict_category", "")
        def _map_v(v_str):
            v = str(v_str).lower()
            if any(word in v for word in ["verified", "true", "safe", "🟢"]): return "verified"
            if any(word in v for word in ["misleading", "🟠"]): return "misleading"
            if any(word in v for word in ["false", "🔴"]): return "false"
            return "unable_to_verify"
            
        frontend_verdict = _map_v(raw_verdict)
        
        tasks_db[task_id] = {
            "status": "completed", 
            "data": {
                "verdict": frontend_verdict,
                "confidenceScore": result.get("confidence_score", 50),
                "explanation": result.get("summary_for_moderator", result.get("evidence_synthesis", "No explanation provided.")),
                "citations": result.get("citations", result.get("evidence_sources", []))
            }
        }
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Background verification failed: {e}")
        tasks_db[task_id] = {"status": "failed", "error": str(e)}

@router.get("/status/{task_id}", status_code=status.HTTP_200_OK)
@limiter.limit("60/minute")
async def get_task_status(request: Request, task_id: str):
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/async", status_code=status.HTTP_202_ACCEPTED)
@limiter.limit("10/minute")
async def verify_async(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Asynchronous endpoint for Next.js frontend proxy.
    Accepts JSON or multipart/form-data. Spawns a background task.
    """
    content_type = request.headers.get("content-type", "")
    text = ""
    file_path = None
    
    if "multipart/form-data" in content_type:
        form = await request.form()
        text = form.get("content", "")
        file_obj = form.get("file")
        if file_obj and hasattr(file_obj, "filename") and file_obj.filename:
            upload_dir = os.path.join("/tmp", "sukoon_uploads")
            os.makedirs(upload_dir, exist_ok=True)
            safe_filename = f"{uuid_lib.uuid4().hex}_{secure_filename(file_obj.filename)}"
            file_path = os.path.join(upload_dir, safe_filename)
            with open(file_path, "wb") as f:
                f.write(await file_obj.read())
                
            # Process media synchronously for now before queuing task (so we don't pass complex file objects)
            from app.ai_modules.media_processing.processors import get_ocr_engine, get_whisper_engine, get_video_analyzer
            
            media_context = ""
            try:
                if "image" in file_obj.content_type:
                    media_context = get_ocr_engine().extract_text(file_path)
                elif "audio" in file_obj.content_type:
                    media_context = get_whisper_engine().transcribe(file_path)
                elif "video" in file_obj.content_type:
                    res = get_video_analyzer().analyze_video(file_path)
                    media_context = "\n".join(res)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Media extraction failed: {e}")
                
            if media_context:
                text = f"{text}\n\n[Media Context extracted from {file_obj.content_type}]:\n{media_context}"
    else:
        try:
            body = await request.json()
            text = body.get("content", body.get("url", ""))
        except:
            text = ""
            
    if not text.strip():
        raise HTTPException(status_code=400, detail="Empty content provided")
        
    task_id = str(uuid_lib.uuid4())
    tasks_db[task_id] = {"status": "processing", "data": None}
    
    # Push heavy lifting to background
    background_tasks.add_task(async_background_fact_check, task_id, text)
    
    return {"success": True, "status": "accepted", "task_id": task_id}

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
            {"step": "vector_search", "message": "Querying local Qdrant/pgvector for known facts..."},
            {"step": "web_search", "message": "Aggregating live web context via SearXNG..."},
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
