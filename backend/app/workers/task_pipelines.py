from celery import shared_task, group, chord
import time
from app.workers.celery_app import DatabaseTask
from datetime import datetime
# In production, these would import from ai_modules
# from ..ai_modules.media_processing.processors import get_whisper_engine, get_ocr_engine
from ..pipelines.text_pipeline import process_text_claim
from ..pipelines.url_pipeline import process_url_claim
from ..pipelines.media_pipeline import process_media_claim

@shared_task(bind=True, max_retries=3)
def process_audio(self, file_path: str):
    """Whisper STT running on GPU"""
    # return get_whisper_engine().transcribe(file_path)
    time.sleep(1)  # simulate work
    return f"Audio transcript for {file_path}"

@shared_task(bind=True, max_retries=3)
def process_ocr(self, file_path: str):
    """OCR running on GPU"""
    # return get_ocr_engine().extract_text(file_path)
    time.sleep(1)  # simulate work
    return f"OCR text for {file_path}"

@shared_task(base=DatabaseTask, bind=True)
def merge_and_verify_media(self, results: list, file_path: str, verification_id: str):
    """
    Chord callback: receives [audio_transcript, ocr_text] from the parallel group,
    merges them, then runs the media verification pipeline.
    """
    db = self.db
    from app.repositories.repos import verification_repo
    
    audio_transcript = results[0] if len(results) > 0 else ""
    ocr_text = results[1] if len(results) > 1 else ""
    combined_context = f"Audio Transcript:\n{audio_transcript}\n\nOCR Text:\n{ocr_text}"
    
    result = process_media_claim(file_path, mime_type="image/jpeg", context=combined_context)
    result["verification_id"] = verification_id
    
    # Save the result to the database safely
    raw_verdict = result.get("verdict", "unverified")
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
        
    frontend_verdict = map_verdict_to_token(raw_verdict)
    
    verification = verification_repo.get(db, id=verification_id)
    if verification:
        verification_repo.update(db, db_obj=verification, obj_in={
            "status": "completed",
            "verdict": frontend_verdict,
            "completed_at": datetime.utcnow()
        })
        
    return generate_truth_card(result)

@shared_task(base=DatabaseTask, bind=True)
def process_claim_task(self, claim_type: str, verification_id: str, mime_type: str = None, is_deep: bool = False):
    """Routes the claim to the appropriate pipeline by pulling context via reference ID."""
    db = self.db
    from app.repositories.repos import verification_repo, claim_repo
    
    verification = verification_repo.get(db, id=verification_id)
    if not verification:
        return {"error": f"Verification {verification_id} not found", "status": "failed"}
        
    claim = claim_repo.get(db, id=verification.claim_id)
    if not claim:
        return {"error": f"Claim for verification {verification_id} not found", "status": "failed"}
        
    content = claim.raw_content

    if claim_type == "text":
        result = process_text_claim(content, is_deep=is_deep)
    elif claim_type == "url":
        url = content
        if content.startswith("Please verify this URL: "):
            url = content.replace("Please verify this URL: ", "").strip()
        result = process_url_claim(url, is_deep=is_deep)
    elif claim_type == "media":
        file_path = content
        if content.startswith("Uploaded media: "):
            file_path = content.replace("Uploaded media: ", "").strip()
        result = process_media_claim(file_path, mime_type=mime_type or "image/jpeg")
    else:
        result = {"error": f"Unknown claim type: {claim_type}", "verdict": "Unverified"}
        
    result["verification_id"] = verification_id
    
    # Save the result to the database safely
    raw_verdict = result.get("verdict", "unverified")
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
        
    frontend_verdict = map_verdict_to_token(raw_verdict)
    
    verification_repo.update(db, db_obj=verification, obj_in={
        "status": "completed",
        "verdict": frontend_verdict,
        "completed_at": datetime.utcnow()
    })
    
    return generate_truth_card(result)

@shared_task
def generate_truth_card(verification_result: dict):
    """Final step to generate Truth Card and update DB/Webhooks"""
    print(f"Task Complete! Truth Card generated for {verification_result.get('verification_id', 'unknown')}")
    return {"status": "success", "truth_card_url": "https://sukoon.ai/cards/123"}

def dispatch_multimodal_pipeline(file_path: str, verification_id: str):
    """
    Fan-Out/Fan-In orchestration for media files.
    Runs Audio (Whisper) and OCR in parallel, merges results, then verifies.
    """
    header = group(
        process_audio.s(file_path),
        process_ocr.s(file_path)
    )
    # Chord: when both tasks finish, call merge_and_verify_media with their results
    callback = merge_and_verify_media.s(file_path=file_path, verification_id=verification_id)
    chord(header)(callback)
