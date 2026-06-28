from pydantic import BaseModel, Field
from typing import List
from enum import Enum

class VerdictDecision(str, Enum):
    TRUE = "true"
    FALSE = "false"
    MISLEADING = "misleading"
    UNVERIFIED = "unverified"

class VerificationResult(BaseModel):
    verdict: VerdictDecision
    confidence_score: float = Field(..., description="Confidence score from 0.0 to 1.0")
    matched_context: str = Field(..., description="The real context retrieved from the vector database")
    source_urls: List[str] = Field(default_factory=list, description="List of reliable sources backing the verdict")

class ContextVerificationAgent:
    """
    Agent responsible for taking extracted claims, querying the Qdrant Vector DB, 
    and using RAG to determine the truthfulness of the claim.
    """
    def __init__(self, model_name: str = "gpt-4o", qdrant_client=None):
        self.model_name = model_name
        self.qdrant_client = qdrant_client # Placeholder for actual client

    async def run(self, claim_text: str) -> VerificationResult:
        """
        Executes the RAG verification pipeline.
        1. Embeds the claim_text
        2. Queries Qdrant for nearest fact chunks
        3. Prompts LLM to evaluate the claim against retrieved context
        """
        print(f"[ContextVerificationAgent] Verifying claim: {claim_text}")
        
        # Mocking the RAG process for MVP architecture
        return VerificationResult(
            verdict=VerdictDecision.MISLEADING,
            confidence_score=0.98,
            matched_context="The referenced audio is from a 2020 lockdown drill and does not apply to the current situation. Local health authorities have confirmed no lockdowns are planned.",
            source_urls=["https://www.who.int", "https://local-health-ministry.gov"]
        )
