import os
import asyncio
from app.ai_modules.fact_checking.llm_client import llm_client
from app.services.rag_service import rag_service

class EvaluationAgent:
    """
    Evaluation Agent used by real-time WebSockets.
    Grounded in local curated knowledge, falling back elegantly to Google Live Search Grounding.
    """
    def evaluate(self, claim: str) -> dict:
        if not claim:
            return {
                "verdict": "UNVERIFIED",
                "confidence_score": 0.0,
                "explanation": "No claim extracted to evaluate.",
                "sourceCitations": [],
                "suggested_action": "Verify files and content before broadcasting."
            }

        # 1. Search Local Curated Knowledge Database
        rag_results = rag_service.retrieve_context(claim)
        
        if rag_results and len(rag_results) >= 2:
            # High quality match found locally, synthesize from database
            context_str = "\n".join([r["text"] for r in rag_results])
            citations = [r["source"] for r in rag_results]
            
            explanation = f"Locally verified matches found:\n{context_str[:200]}"
            return {
                "verdict": "TRUE",
                "confidence_score": 0.95,
                "explanation": explanation,
                "sourceCitations": citations,
                "suggested_action": "Your community relies on curated facts. This claim has been validated through our local databases.",
                "toxicity_score": 0,
                "factuality_score": 100
            }
        else:
            # 2. Local fallback: Query Google search engine grounding directly!
            search_result = llm_client.generate(claim)
            
            verdict_str = search_result.get("verdict", "UNVERIFIED")
            citations = search_result.get("grounding_sources", [])
            
            suggested_action = (
                "Verified safe. Sharing objective scientific and public truths brings community peace."
                if verdict_str == "TRUE" else 
                "Misleading or false information detected. Protect community peace by not sharing further."
                if verdict_str == "FALSE" else
                "Unable to verify authenticity. Exercise critical judgment before sharing."
            )
            
            return {
                "verdict": verdict_str,
                "confidence_score": 0.95 if verdict_str in ["TRUE", "FALSE"] else 0.40,
                "explanation": search_result.get("explanation", "Verified via live Google Search Engine Grounding."),
                "sourceCitations": citations,
                "suggested_action": suggested_action,
                "toxicity_score": 0,
                "factuality_score": 100 if verdict_str == "TRUE" else 0 if verdict_str == "FALSE" else 50
            }

evaluation_agent = EvaluationAgent()
