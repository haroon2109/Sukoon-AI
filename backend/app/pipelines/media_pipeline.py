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
    """Processes a media claim by uploading it and sending it to the multimodal LLM."""
    
    # 1. Metadata Extraction and Validation
    if mime_type not in ALLOWED_MIME_TYPES:
        return {"error": f"Unsupported media type: {mime_type}", "verdict": "Unverified"}
    
    # 2. Storage Hand-off
    gcs_uri = upload_to_gcs(file_path, mime_type)
    
    # 3. Analyze using multimodal LLM (Gemini Flash)
    result = llm_client.analyze_media(file_path=gcs_uri, mime_type=mime_type, context=context)
    
    return result
