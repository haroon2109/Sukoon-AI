from sqlalchemy.orm import Session
from ..repositories.repos import claim_repo, verification_repo
from ..domain.schemas.schemas import ClaimCreate, EvidenceSourceSchema, VerdictCategory, RecommendedAction
from ..ai_modules.fact_checking.claim_extraction import ClaimExtractionAgent
from ..ai_modules.rag.evidence_retrieval import EvidenceRetrievalAgent
from ..ai_modules.fact_checking.fact_verification import FactVerificationAgent
from ..ai_modules.fact_checking.perspective_agent import PerspectiveAgent
from ..ai_modules.fact_checking.shieldgemma_agent import ShieldGemmaAgent
from ..ai_modules.fact_checking.synthid_agent import SynthIDAgent
import uuid

class AgenticWorkflowCoordinator:
    def __init__(self):
        self.toxicity_filter = PerspectiveAgent()
        self.safety_filter = ShieldGemmaAgent()
        self.claim_extractor = ClaimExtractionAgent()
        self.evidence_retriever = EvidenceRetrievalAgent()
        self.fact_verifier = FactVerificationAgent()
        self.synthid_watermarker = SynthIDAgent()

    def ingest_payload(self, db: Session, claim_in: ClaimCreate, user_id: str):
        # 1. Save Raw Claim
        new_claim = claim_repo.create(db, {
            "user_id": user_id,
            "raw_content": claim_in.raw_content,
            "language": claim_in.language
        })
        
        # 2. Create Pending Verification Record
        new_verification = verification_repo.create(db, {
            "claim_id": new_claim.id,
            "user_id": user_id,
            "status": "pending"
        })
        
        # 3. Synchronous verification for MVP removed - handled by WebSocket
        return new_verification

    async def process_verification(self, text: str):
        """
        Coordinates the autonomous agents to execute the full AI verification workflow.
        """
        # 0. Early Toxicity Check (Perspective API)
        toxicity_score = await self.toxicity_filter.analyze_toxicity(text)
        if toxicity_score >= 0.80:
            return {
                "summary_for_moderator": f"Post flagged for high toxicity/abusive language by Perspective API (Score: {toxicity_score:.2f}).",
                "verdict_category": VerdictCategory.TOXIC,
                "recommended_action": RecommendedAction.REMOVE,
                "confidence_score": toxicity_score,
                "evidence_synthesis": "Workflow short-circuited due to severe toxicity.",
                "counter_narrative_suggestion": None,
                "citations": [],
                "evidence_sources": []
            }
            
        # 0.5. Safety Policy Check (ShieldGemma)
        safety_report = await self.safety_filter.check_compliance(text)
        if not safety_report["is_safe"]:
            policies = ", ".join(safety_report["violated_policies"])
            return {
                "summary_for_moderator": f"Prompt rejected by ShieldGemma for violating safety policies: {policies}.",
                "verdict_category": VerdictCategory.TOXIC,
                "recommended_action": RecommendedAction.REMOVE,
                "confidence_score": 0.95,
                "evidence_synthesis": "Workflow short-circuited due to safety policy violation.",
                "counter_narrative_suggestion": None,
                "citations": [],
                "evidence_sources": []
            }

        import asyncio
        from ..core.logger import api_logger
        
        # 1. Extract Claims
        try:
            claims = await asyncio.wait_for(self.claim_extractor.extract(text), timeout=30.0)
        except asyncio.TimeoutError:
            api_logger.error("Claim extraction timed out.")
            claims = []
        
        # 2. Retrieve Evidence
        try:
            evidence = await asyncio.wait_for(self.evidence_retriever.retrieve(claims), timeout=45.0)
        except asyncio.TimeoutError:
            api_logger.error("Evidence retrieval timed out.")
            evidence = []
        
        # 3. Verify Facts
        try:
            report_data = await asyncio.wait_for(self.fact_verifier.verify(claims, evidence), timeout=60.0)
        except asyncio.TimeoutError:
            api_logger.error("Fact verification timed out.")
            report_data = {
                "summary_for_moderator": "Verification timed out due to high load or complex reasoning requirements.",
                "verdict_category": VerdictCategory.NEEDS_MORE_EVIDENCE,
                "recommended_action": RecommendedAction.FLAG,
                "confidence_score": 0.0,
                "evidence_synthesis": "The reasoning model took too long to respond.",
                "counter_narrative_suggestion": None,
                "citations": []
            }
        
        # 4. Apply SynthID Watermark to generated text
        if "summary_for_moderator" in report_data and report_data["summary_for_moderator"]:
            report_data["summary_for_moderator"] = self.synthid_watermarker.apply_watermark(report_data["summary_for_moderator"])
            
        if report_data.get("counter_narrative_suggestion"):
            report_data["counter_narrative_suggestion"] = self.synthid_watermarker.apply_watermark(report_data["counter_narrative_suggestion"])
        
        return {
            "summary_for_moderator": report_data["summary_for_moderator"],
            "verdict_category": report_data["verdict_category"],
            "recommended_action": report_data["recommended_action"],
            "confidence_score": report_data["confidence_score"],
            "evidence_synthesis": report_data["evidence_synthesis"],
            "counter_narrative_suggestion": report_data.get("counter_narrative_suggestion"),
            "citations": report_data.get("citations", []),
            "evidence_sources": evidence
        }

agentic_workflow_coordinator = AgenticWorkflowCoordinator()
