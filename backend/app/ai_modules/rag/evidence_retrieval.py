from typing import List
from app.domain.schemas.schemas import ExtractedClaim, RetrievedEvidence
from app.services.rag_service import rag_service
from app.services.reranker import rerank_results
from app.providers.search_provider import search_provider

class EvidenceRetrievalAgent:
    def __init__(self):
        pass

    async def retrieve(self, claims: List[ExtractedClaim]) -> List[RetrievedEvidence]:
        """
        Autonomous agent that retrieves evidence relevant to the given claims using 
        real-time DuckDuckGo Search and local RAG.
        """
        evidence_list = []
        for claim in claims:
            raw_results = []
            
            # 1. Fetch real-time web evidence (Primary)
            search_results = search_provider.search(claim.claim_text, max_results=5)
            for sr in search_results:
                raw_results.append({
                    "text": sr["snippet"],
                    "url": sr["link"],
                    "title": sr["title"],
                    "source": "Web Search"
                })
                
            # 2. Retrieve local knowledge base context (Secondary)
            local_results = rag_service.retrieve_context(claim.claim_text, top_k=5)
            raw_results.extend(local_results)
            
            if not raw_results:
                continue
                
            # 3. Rerank the combined results down to top 3
            reranked = rerank_results(claim.claim_text, raw_results, top_k=3)
            
            for doc in reranked:
                evidence = RetrievedEvidence(
                    source_url=doc.get("url", doc.get("source_url", "https://example.com/source")),
                    content=doc.get("text", doc.get("content", doc.get("title", "No content available"))),
                    relevance_score=doc.get("rerank_score", doc.get("similarity", 0.0))
                )
                evidence.credibility_score = doc.get("credibility_score", "Unknown")
                evidence_list.append(evidence)
            
        return evidence_list
