from pydantic import BaseModel, Field
from typing import List, Optional
import json

class Evidence(BaseModel):
    source_name: str = Field(description="Name of the trusted source (e.g., PIB Fact Check, Alt News).")
    evidence_text: str = Field(description="The contextual facts retrieved from the source.")
    url: Optional[str] = Field(description="Link to the original fact-check article.", default=None)
    relevance_score: float = Field(description="Vector similarity score between claim and evidence.")

class VerificationResult(BaseModel):
    verdict: str = Field(description="Must be 'verified', 'misleading', or 'false'.")
    confidence: float = Field(description="Final calculated confidence score (0.0 to 1.0).")
    supporting_evidence: List[Evidence] = Field(description="List of evidence used to reach the verdict.")
    verified_context: str = Field(description="A synthesized explanation of the facts.")

class RAGVerificationAgent:
    def __init__(self):
        # In production, initialize QdrantClient and Embedding models here
        self.vector_db_ready = True
        
    def _search_vector_db(self, extracted_claim: dict) -> List[Evidence]:
        """
        Simulates querying Qdrant/Pinecone with the embedded claim.
        Returns the top K chunks of evidence from our trusted sources.
        """
        claim_text = extracted_claim.get("claim", "").lower()
        
        # Simulated RAG hits based on keywords
        if "chennai" in claim_text:
            return [
                Evidence(
                    source_name="BOOM Live",
                    evidence_text="The video circulating is from an old political rally in 2018, not recent violence. Chennai police have confirmed the city is peaceful.",
                    url="https://boomlive.in/fake-news/chennai-violence-video",
                    relevance_score=0.94
                )
            ]
        elif "rbi" in claim_text or "1000" in claim_text:
            return [
                Evidence(
                    source_name="PIB Fact Check",
                    evidence_text="The Reserve Bank of India (RBI) has not issued any new Rs 1000 currency notes. Images circulating online are digitally altered.",
                    url="https://pib.gov.in/factcheck/rbi-notes",
                    relevance_score=0.99
                )
            ]
            
        # Default empty return for unverified claims
        return []

    def verify_claim(self, extracted_claim: dict) -> dict:
        """
        Core Verification Logic:
        1. Search Evidence (Vector Search)
        2. Compare Claims against retrieved context
        3. Calculate Confidence
        """
        
        # Step 1: Retrieve Sources
        evidence_list = self._search_vector_db(extracted_claim)
        
        # Step 2 & 3: Compare Claims and Calculate Confidence
        # In production, an LLM evaluates the `evidence_list` against the `extracted_claim`
        
        if not evidence_list:
            # If no evidence is found in the database, we cannot verify it
            result = VerificationResult(
                verdict="unverified",
                confidence=0.0,
                supporting_evidence=[],
                verified_context="We could not find matching fact-checks for this claim in our trusted databases."
            )
            return result.model_dump()
            
        # Simulated Synthesis
        primary_evidence = evidence_list[0]
        
        result = VerificationResult(
            verdict="false", # Based on our mock data, both scenarios are false
            confidence=primary_evidence.relevance_score,
            supporting_evidence=evidence_list,
            verified_context=f"According to {primary_evidence.source_name}, {primary_evidence.evidence_text.lower()}"
        )
        
        return result.model_dump()

if __name__ == "__main__":
    # Test the RAG agent
    agent = RAGVerificationAgent()
    
    sample_claim = {
        "claim": "Violence is currently occurring in the city.",
        "location": "Chennai",
        "date": "Today",
        "confidence": 0.92
    }
    
    print(f"Input Claim: {json.dumps(sample_claim, indent=2)}\n")
    print("Verification Process Output:")
    print(json.dumps(agent.verify_claim(sample_claim), indent=2))
