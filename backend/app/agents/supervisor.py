import logging
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel, Field

# Import the correct classes from agents module
from .verification_agent import RAGVerificationAgent
from .context_verifier import ContextVerificationAgent
from .peace_agent import PeaceResponseAgent
from .claim_extractor import ClaimExtractorAgent

logger = logging.getLogger(__name__)

class OrchestrationResult(BaseModel):
    status: str = Field(description="The final status of the orchestrated task: 'success' or 'error'")
    verdict: str = Field(description="Must be 'verified', 'misleading', or 'false'.", default="unverified")
    confidence: float = Field(description="Confidence score (0.0 to 1.0)", default=0.0)
    summary: str = Field(description="Summary of the agent's findings", default="")
    trace: List[str] = Field(description="List of steps taken by the supervisor", default_factory=list)

def _run_sync(coro):
    """Helper to run async coroutines synchronously in Celery worker thread."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    if loop.is_running():
        # Event loop already running, execute via a separate thread pool to avoid blocking
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(asyncio.run, coro)
            return future.result()
    else:
        return loop.run_until_complete(coro)

class SupervisorAgent:
    """
    Central Orchestrator that receives an incoming claim, delegates to specific
    agents (Extraction -> Vector Search -> Synthesis), and returns a unified result.
    This replaces complex LangGraph routing for MVP and is built to be easily integrated
    with Google ADK tools.
    """
    
    def __init__(self):
        self.claim_extractor = ClaimExtractorAgent()
        self.rag_verifier = RAGVerificationAgent()
        self.context_verifier = ContextVerificationAgent()
        self.peace_agent = PeaceResponseAgent()
        
    def process_request(self, raw_input: str, user_context: dict = None) -> dict:
        """
        Main entry point for verifying a suspicious URL or text.
        """
        trace = []
        try:
            # Step 1: Extract Claim
            trace.append("Starting claim extraction")
            extracted_claim = _run_sync(self.claim_extractor.extract(raw_input))
            if not extracted_claim or not extracted_claim.get("claim"):
                return OrchestrationResult(
                    status="error",
                    summary="Could not extract a verifiable claim from the input.",
                    trace=trace
                ).model_dump()
                
            trace.append(f"Claim extracted: {extracted_claim.get('claim')}")
            
            # Step 2: Verification via RAG
            trace.append("Delegating to RAGVerificationAgent for vector search and synthesis")
            verification_result = self.rag_verifier.verify_claim(extracted_claim)
            
            # Step 3: Context & Nuance Verification (Optional parallel step)
            trace.append("Cross-checking with ContextVerifierAgent")
            context_result = _run_sync(self.context_verifier.run(extracted_claim.get("claim", "")))
            
            trace.append("Verification complete")
            
            # Extract explanation/context safely
            matched_context = ""
            if context_result:
                matched_context = getattr(context_result, 'matched_context', '')
            if not matched_context:
                matched_context = verification_result.get("verified_context", "")
            
            # Construct Final Result
            return OrchestrationResult(
                status="success",
                verdict=verification_result.get("verdict", "unverified"),
                confidence=verification_result.get("confidence", 0.0),
                summary=matched_context,
                trace=trace
            ).model_dump()
            
        except Exception as e:
            logger.error(f"Error in supervisor orchestration: {e}")
            trace.append(f"Error: {str(e)}")
            return OrchestrationResult(
                status="error",
                summary="An internal orchestration error occurred.",
                trace=trace
            ).model_dump()
# Singleton instance exported for use across the application
supervisor = SupervisorAgent()

if __name__ == "__main__":
    result = supervisor.process_request("URGENT: RBI has released new Rs 1000 notes!")
    print(result)
