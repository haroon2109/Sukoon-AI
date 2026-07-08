import logging
from typing import List
from app.domain.schemas.schemas import ExtractedClaim, ExtractedClaimsList
from app.providers.reasoning_provider import ProviderFactory

logger = logging.getLogger(__name__)

class ClaimExtractionAgent:
    def __init__(self):
        pass

    async def extract(self, text: str) -> List[ExtractedClaim]:
        """
        Autonomous agent that uses the ReasoningProvider to identify and extract verifiable claims from raw text.
        """
        if not text.strip():
            return []
            
        system_instruction = (
            f"Extract all distinct, verifiable claims from the following text. "
            f"Provide the claim text and a brief context for each. "
            f"Ignore opinions, jokes, sarcasm, and personal thoughts.\n"
            f"Respond ONLY with a valid JSON object matching this schema:\n"
            f'{{"claims": [{{"claim_text": "string", "context": "string"}}]}}'
        )
        
        from app.core.payload_optimizer import PayloadOptimizer
        provider = ProviderFactory.get_provider()
        optimized_text = PayloadOptimizer.optimize_text(text, max_chars=provider.capabilities.max_context_window * 3) # conservative char limit
        prompt = f"Text:\n{optimized_text}"
        
        try:
            result = await provider.generate_json(prompt, system_instruction=system_instruction)
            
            if "error" in result:
                logger.error(f"Error from provider during claim extraction: {result['error']}")
                return []
                
            claims_list = ExtractedClaimsList(**result)
            return claims_list.claims
        except Exception as e:
            logger.error(f"Error in ClaimExtractionAgent: {e}")
            return []
