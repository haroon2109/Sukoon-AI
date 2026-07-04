import os
import uuid
import logging
from ..ai_modules.fact_checking.llm_client import llm_client

logger = logging.getLogger(__name__)

ALLOWED_MIME_TYPES = {
    "image/jpeg", "image/png", "image/webp",
    "video/mp4", "video/webm", "video/quicktime"
}

def upload_to_gcs(file_path: str, mime_type: str) -> str:
    """Uploads a file to Google Cloud Storage and returns the gs:// URI."""
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        logger.warning("GCS_BUCKET_NAME not set. Falling back to local file path for Gemini API.")
        return file_path
        
    try:
        from google.cloud import storage
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        
        # Generate a unique blob name based on original filename extension
        ext = os.path.splitext(file_path)[1]
        blob_name = f"media_claims/{uuid.uuid4()}{ext}"
        
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path, content_type=mime_type)
        
        gcs_uri = f"gs://{bucket_name}/{blob_name}"
        logger.info(f"File uploaded to GCS: {gcs_uri}")
        return gcs_uri
    except Exception as e:
        logger.error(f"Failed to upload to GCS: {e}")
        # Fall back to local file path if GCS fails but we still want to test Gemini
        return file_path

def process_media_claim(file_path: str, mime_type: str, context: str = "") -> dict:
    """Processes a media claim by running it through sequential sub-modules with engine-level fault isolation."""
    
    # 1. Metadata Extraction and Validation
    if mime_type not in ALLOWED_MIME_TYPES:
        return {"error": f"Unsupported media type: {mime_type}", "verdict": "Unverified"}
    
    submodule_results = {}
    
    # Engine A: Storage Hand-off
    gcs_uri = file_path
    try:
        gcs_uri = upload_to_gcs(file_path, mime_type)
        submodule_results["gcs_upload"] = {"status": "success", "uri": gcs_uri}
    except Exception as e:
        logger.error(f"[Media Pipeline] GCS Upload failed: {e}", exc_info=True)
        submodule_results["gcs_upload"] = {"status": "failed", "error": str(e)}
        
    # Engine B: Metadata Auditing Heuristics
    try:
        file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
        submodule_results["metadata_audit"] = {"status": "success", "file_size": file_size}
    except Exception as e:
        logger.error(f"[Media Pipeline] Metadata audit failed: {e}", exc_info=True)
        submodule_results["metadata_audit"] = {"status": "failed", "error": str(e)}
        
    # Engine C: Multimodal AI Inference (Gemini Flash)
    ai_result = {}
    try:
        ai_result = llm_client.analyze_media(file_path=gcs_uri, mime_type=mime_type, context=context)
        submodule_results["multimodal_ai"] = {"status": "success", "output": ai_result}
    except Exception as e:
        logger.error(f"[Media Pipeline] Multimodal AI Analysis failed: {e}", exc_info=True)
        submodule_results["multimodal_ai"] = {"status": "failed", "error": str(e)}
        ai_result = {
            "verdict": "unable_to_verify",
            "confidence_score": 0.0,
            "explanation": f"AI evaluation engine encountered a failure: {str(e)}"
        }
        
    # Compile final report with isolated sub-module statuses
    final_report = {
        "verdict": ai_result.get("verdict", "unable_to_verify"),
        "confidence_score": ai_result.get("confidence_score", 0.0),
        "explanation": ai_result.get("explanation", "AI verification engine was offline/unavailable."),
        "submodule_metrics": submodule_results
    }
    
    return final_report
