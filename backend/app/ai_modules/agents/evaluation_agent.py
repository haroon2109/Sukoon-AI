import logging
from ..data_fetching.web_search import search_web
from ..fact_checking.llm_client import llm_client
from ..rag.qdrant_client import qdrant_client
from ...core.cache_layer import cache

logger = logging.getLogger(__name__)

class EvaluationAgent:
    def __init__(self):
        pass

    def _extract_core_claim(self, text: str) -> str:
        """Uses a fast model to extract the core claim from a block of text."""
        prompt = f"""
        Extract the core, checkable claim from the following text. 
        Respond with a JSON object containing a single key "claim".
        Text: {text}
        """
        result = llm_client.generate(prompt, model_type="flash")
        return result.get("claim", text)

    def _generate_search_queries(self, claim: str) -> list:
        """Agentic workflow: generates 3 distinct search angles."""
        prompt = f"""
        Given the following claim, generate exactly 3 distinct search queries to thoroughly investigate it.
        Consider different angles: 
        1. Verifying the core event/facts.
        2. Finding existing fact-checks or debunkings.
        3. Checking the credibility of the source or identifying context (e.g. image origin).
        
        Respond with a JSON object containing a single key "queries" which is a list of 3 strings.
        Claim: "{claim}"
        """
        result = llm_client.generate(prompt, model_type="flash")
        return result.get("queries", [claim])

    def evaluate(self, text: str) -> dict:
        """
        The orchestrator method for Intelligent Evaluation.
        1. Check Cache for exact match.
        2. Extract the claim.
        3. Query RAG (internal DB).
        4. Query Web Search (live web).
        5. Synthesize with the Reasoning Model.
        """
        # Step 1: Check Cache
        cached_result = cache.get(text)
        if cached_result:
            logger.info("Serving evaluation from cache.")
            return cached_result
            
        # Step 2: Extract claim
        core_claim = self._extract_core_claim(text)
        logger.info(f"Core claim extracted: {core_claim}")

        # Step 2: Fetch internal knowledge (RAG)
        rag_results = qdrant_client.search_similar_text(core_claim)
        rag_context = "\n".join([f"- {r['payload']['evidence_text']} (Source: {r['payload']['source_name']})" for r in rag_results])
        
        # Step 3: Fetch live web context
        web_results = search_web(core_claim)
        web_context = "\n".join([f"- {r['snippet']} (Source: {r['title']})" for r in web_results])
        
        # Step 4: Synthesize Final Evaluation using Reasoning Model
        synthesis_prompt = f"""
        You are the core analysis engine of Sukoon AI, a platform dedicated to fostering community peace by debunking hate speech and fake news. Analyze the input strictly for: 
        1) Verifiable misinformation
        2) Incitement to hatred or violence against any community
        3) Sentiment toxicity
        
        Claim: "{core_claim}"
        Original Text: "{text}"
        
        Internal Knowledge Base (Verified):
        {rag_context}
        
        Live Web Search Results:
        {web_context}
        
        Respond ONLY in a valid JSON format with the keys: 
        - 'verdict' (Safe, Misleading, Toxic)
        - 'confidence_score' (0.0 to 1.0)
        - 'explanation' (a concise, neutral summary of the facts)
        - 'flags' (an array of categories triggered, e.g., ["misinformation", "hate speech"])
        - 'toxicity_score' (Integer 0-100: How aggressively the piece tries to incite anger)
        - 'factuality_score' (Integer 0-100: How much can be cross-verified by reputable sources)
        - 'community_impact_rating' (Integer 0-100: Is this targeting vulnerable groups or disrupting peace?)
        - 'peace_verdict' (High Risk, Moderate Risk, Safe)
        - 'suggested_action' (Actionable advice, e.g., "Do not share.")
        """
        
        evaluation = llm_client.generate(synthesis_prompt, model_type="pro")
        
        # Merge sources for TruthCard
        sources = []
        
        # Add DuckDuckGo sources
        for r in web_results:
            if 'link' in r:
                sources.append(r['link'])
                
        # Add Google Search Grounding sources
        if 'grounding_sources' in evaluation:
            sources.extend(evaluation['grounding_sources'])
            
        evaluation['sourceCitations'] = list(set(sources))
        
        # Save to cache before returning
        if "error" not in evaluation:
            cache.set(text, evaluation)
            
        return evaluation

    def deep_evaluate(self, text: str) -> dict:
        """
        Agentic Deep Research pipeline.
        1. Extract claim.
        2. Generate 3 distinct queries.
        3. Aggregate multi-query search results.
        4. Synthesize looking for structural inconsistencies.
        """
        # Step 1: Check Cache (append _deep to key so it doesn't mix with standard eval)
        cache_key = f"{text}_deep"
        cached_result = cache.get(cache_key)
        if cached_result:
            logger.info("Serving deep evaluation from cache.")
            return cached_result
            
        # Step 2: Extract claim
        core_claim = self._extract_core_claim(text)
        logger.info(f"[Deep Scan] Core claim extracted: {core_claim}")

        # Step 3: Generate multi-queries
        queries = self._generate_search_queries(core_claim)
        logger.info(f"[Deep Scan] Generated queries: {queries}")
        
        # Fetch RAG
        rag_results = qdrant_client.search_similar_text(core_claim)
        rag_context = "\n".join([f"- {r['payload']['evidence_text']} (Source: {r['payload']['source_name']})" for r in rag_results])
        
        # Execute multi-query web search
        all_web_results = []
        for q in queries:
            all_web_results.extend(search_web(q))
            
        web_context = "\n".join([f"- {r['snippet']} (Source: {r['title']})" for r in all_web_results])
        
        # Step 4: Deep Synthesis
        synthesis_prompt = f"""
        You are the core analysis engine of Sukoon AI conducting a DEEP SCAN. 
        Analyze the input strictly for: 
        1) Verifiable misinformation
        2) Incitement to hatred or violence against any community
        3) Sentiment toxicity
        
        CRITICAL INSTRUCTION: You must actively look for and point out structural inconsistencies in the 'explanation' field. 
        For example: "The article claims this happened today, but sources indicate this photo is actually from 2021" or "The text misattributes this quote to X, when it was originally said by Y."
        
        Claim: "{core_claim}"
        Original Text: "{text}"
        
        Internal Knowledge Base (Verified):
        {rag_context}
        
        Aggregated Deep Web Search Results:
        {web_context}
        
        Respond ONLY in a valid JSON format with the keys: 
        - 'verdict' (Safe, Misleading, Toxic)
        - 'confidence_score' (0.0 to 1.0)
        - 'explanation' (a concise, neutral summary of the facts highlighting any structural inconsistencies discovered)
        - 'flags' (an array of categories triggered)
        - 'toxicity_score' (Integer 0-100: How aggressively the piece tries to incite anger)
        - 'factuality_score' (Integer 0-100: How much can be cross-verified by reputable sources)
        - 'community_impact_rating' (Integer 0-100: Is this targeting vulnerable groups or disrupting peace?)
        - 'peace_verdict' (High Risk, Moderate Risk, Safe)
        - 'suggested_action' (Actionable advice, e.g., "Do not share.")
        """
        
        evaluation = llm_client.generate(synthesis_prompt, model_type="pro")
        
        # Merge sources for TruthCard
        sources = []
        for r in all_web_results:
            if 'link' in r:
                sources.append(r['link'])
                
        if 'grounding_sources' in evaluation:
            sources.extend(evaluation['grounding_sources'])
            
        evaluation['sourceCitations'] = list(set(sources))
        
        # Save to cache
        if "error" not in evaluation:
            cache.set(cache_key, evaluation)
            
        return evaluation

evaluation_agent = EvaluationAgent()
