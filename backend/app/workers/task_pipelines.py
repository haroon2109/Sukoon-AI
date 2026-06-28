from celery import shared_task, group, chord
import time
# In production, these would import from ai_modules
# from ..ai_modules.media_processing.processors import whisper_engine, ocr_engine
from ..pipelines.text_pipeline import process_text_claim
from ..pipelines.url_pipeline import process_url_claim
from ..pipelines.media_pipeline import process_media_claim

@shared_task(bind=True, max_retries=3)
def process_audio(self, file_path: str):
    """Whisper STT running on GPU"""
    # return whisper_engine.transcribe(file_path)
    time.sleep(1) # simulate work
    return f"Audio transcript for {file_path}"

@shared_task(bind=True, max_retries=3)
def process_ocr(self, file_path: str):
    """OCR running on GPU"""
    # return ocr_engine.extract_text(file_path)
    time.sleep(1) # simulate work
    return f"OCR text for {file_path}"

@shared_task
def process_claim_task(claim_type: str, content: str, verification_id: str, mime_type: str = None, is_deep: bool = False):
    """Routes the claim to the appropriate pipeline."""
    if claim_type == "text":
        result = process_text_claim(content, is_deep=is_deep)
    elif claim_type == "url":
        result = process_url_claim(content, is_deep=is_deep)
    elif claim_type == "media":
        # For media, content is the file path
        result = process_media_claim(content, mime_type=mime_type or "image/jpeg")
    else:
        result = {"error": f"Unknown claim type: {claim_type}", "verdict": "Unverified"}
        
    result["verification_id"] = verification_id
    return result

@shared_task
def generate_truth_card(verification_result: dict):
    """Final step to generate Truth Card and update DB/Webhooks"""
    # db update logic here
    print(f"Task Complete! Truth Card generated for {verification_result['verification_id']}")
    return {"status": "success", "truth_card_url": "https://sukoon.ai/cards/123"}

def dispatch_multimodal_pipeline(file_path: str, verification_id: str):
    """
    Fan-Out/Fan-In orchestration.
    1. Splits processing into parallel Audio and OCR tasks.
    2. Uses a Chord to wait for both to finish.
    3. Chains the result to extraction, verification, and output.
    """
    header = group(
        process_audio.s(file_path),
        process_ocr.s(file_path)
    )
    
    # Chord: when 'header' group finishes, pass results to the chain
    # We can use process_claim_task for the verification part
    callback = (
        process_claim_task.s("media", file_path, verification_id) | 
        generate_truth_card.s()
    )
    
    chord(header)(callback)
