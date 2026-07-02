from fastapi import APIRouter, Request, HTTPException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/webhook")
async def receive_n8n_webhook(request: Request):
    """
    Endpoint for the self-hosted n8n instance to trigger backend logic.
    For example, n8n can scrape a tweet and send the payload here to trigger a verification run.
    """
    try:
        payload = await request.json()
        logger.info(f"[n8n Webhook] Received automation trigger: {payload}")
        
        # Example: Triggering the verification pipeline for an incoming social media post
        source = payload.get("source", "unknown")
        content = payload.get("content", "")
        
        if not content:
            raise HTTPException(status_code=400, detail="Missing content in webhook payload")
            
        logger.info(f"Triggering verification for {source} content: {content[:50]}...")
        
        # In a real environment, this would call `verification_service.py` or the LangGraph orchestrator
        return {"status": "success", "message": "Workflow triggered successfully", "job_id": "job_n8n_example"}
        
    except Exception as e:
        logger.error(f"Error processing n8n webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal webhook processing error")
