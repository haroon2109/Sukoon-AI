from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.domain.schemas.schemas import ExplainableAIReport, EvidenceSourceSchema
from app.services.verification_service import agentic_workflow_coordinator
import uuid

router = APIRouter()

class TextVerificationRequest(BaseModel):
    text: str

@router.post("/text", response_model=ExplainableAIReport)
async def verify_text(request: TextVerificationRequest):
    """
    Triggers the Agentic Decision Platform to verify a piece of text.
    Coordinates autonomous agents to extract claims, retrieve evidence, and generate an XAI report.
    """
    try:
        result = await agentic_workflow_coordinator.process_verification(request.text)
        
        # Transform into VerificationResponse (Using mock IDs for now)
        evidence_sources = [
            EvidenceSourceSchema(
                source_name="Retrieved Source",
                evidence_url=e.source_url,
                snippet=e.content,
                match_confidence=e.relevance_score or 0.0
            ) for e in result["evidence_sources"]
        ]
        
        response = ExplainableAIReport(
            id=str(uuid.uuid4()),
            claim_id=str(uuid.uuid4()),
            status="completed",
            summary_for_moderator=result["summary_for_moderator"],
            verdict_category=result["verdict_category"],
            recommended_action=result["recommended_action"],
            confidence_score=result["confidence_score"],
            evidence_synthesis=result["evidence_synthesis"],
            counter_narrative_suggestion=result["counter_narrative_suggestion"],
            evidence_sources=evidence_sources,
            risk_scores=[]
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
