import logging
from ..fact_checking.llm_client import llm_client
from ...core.cache_layer import cache

logger = logging.getLogger(__name__)

class EvaluationAgent:
    def __init__(self):
        pass

    def evaluate(self, text: str) -> dict:
        """
        The orchestrator method for Intelligent Evaluation.
        1. Check Cache for exact match.
        2. Synthesize using Gemini 2.5 Flash with Live Google Search Grounding.
        """
        # Step 1: Check Cache
        cached_result = cache.get(text)
        if cached_result:
            logger.info("Serving evaluation from cache.")
            return cached_result
            
        # Step 2: Synthesize Final Evaluation using Reasoning Model and Grounding
        synthesis_prompt = f"""
        You are an expert, neutral truth-verification entity. Your primary rule is accuracy.
        When evaluating an entry, check global consensus via Google Search.
        Do not assume a statement is false just because it does not appear on a myth-busting portal.
        
        LOGICAL PATHWAY:
        - If the statement accurately reflects established laws, history, or geography, you MUST return 'TRUE' (or Verified).
        - Only return 'FALSE' if your grounding results explicitly state the claim is an intentional hoax or debunked rumor.
        
        Original Text/Claim: "{text}"
        
        Respond ONLY in a valid JSON format with the keys: 
        - 'verdict' (Verified, Misleading, False)
        - 'confidence_score' (0.0 to 1.0)
        - 'explanation' (a concise, neutral summary of the facts based on your live search. YOU MUST explicitly name the fact-checking site (e.g. 'According to AltNews...') you used to reach your conclusion to prove lack of bias)
        - 'flags' (an array of categories triggered, e.g., ["misinformation", "hate speech"])
        - 'toxicity_score' (Integer 0-100: How aggressively the piece tries to incite anger)
        - 'factuality_score' (Integer 0-100: How much can be cross-verified by reputable sources)
        - 'community_impact_rating' (Integer 0-100: Is this targeting vulnerable groups or disrupting peace?)
        - 'peace_verdict' (High Risk, Moderate Risk, Safe)
        - 'suggested_action' (Actionable advice, e.g., "Do not share.")
        """
        
        evaluation = llm_client.generate(synthesis_prompt)
        
        # Merge grounding sources for TruthCard
        sources = []
        if 'grounding_sources' in evaluation:
            sources.extend(evaluation['grounding_sources'])
            
        evaluation['sourceCitations'] = list(set(sources))
        
        # Save to cache before returning
        if "error" not in evaluation:
            cache.set(text, evaluation)
            
        return evaluation

    def deep_evaluate(self, text: str) -> dict:
        """
        Agentic Deep Research pipeline (Now handled entirely by Gemini 2.5 Flash native search).
        """
        cache_key = f"{text}_deep"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info("Serving deep evaluation from cache.")
            return cached_result
            
        synthesis_prompt = f"""
        You are conducting a DEEP SCAN as a neutral truth-verification entity.
        Your primary rule is absolute accuracy based on established global consensus.
        
        LOGICAL PATHWAY:
        - If the statement accurately reflects established laws, history, or geography, you MUST return 'TRUE' (or Verified).
        - Only return 'FALSE' if your grounding results explicitly state the claim is an intentional hoax or debunked rumor.
        - Do not aggressively flag harmless text as toxic or deceptive without explicit proof.
        
        Original Text/Claim: "{text}"
        
        Respond ONLY in a valid JSON format with the keys: 
        - 'verdict' (Verified, Misleading, False)
        - 'confidence_score' (0.0 to 1.0)
        - 'explanation' (a concise, neutral summary of the facts highlighting any structural inconsistencies discovered. YOU MUST explicitly name the fact-checking site used to prove lack of bias)
        - 'flags' (an array of categories triggered)
        - 'toxicity_score' (Integer 0-100: How aggressively the piece tries to incite anger)
        - 'factuality_score' (Integer 0-100: How much can be cross-verified by reputable sources)
        - 'community_impact_rating' (Integer 0-100: Is this targeting vulnerable groups or disrupting peace?)
        - 'peace_verdict' (High Risk, Moderate Risk, Safe)
        - 'suggested_action' (Actionable advice, e.g., "Do not share.")
        """
        
        evaluation = llm_client.generate(synthesis_prompt)
        
        sources = []
        if 'grounding_sources' in evaluation:
            sources.extend(evaluation['grounding_sources'])
            
        evaluation['sourceCitations'] = list(set(sources))
        
        # Save to cache
        if "error" not in evaluation:
            cache.set(cache_key, evaluation)
            
        return evaluation

evaluation_agent = EvaluationAgent()
