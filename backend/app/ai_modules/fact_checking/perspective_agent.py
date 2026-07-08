import os
import json
import httpx
import logging

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.groq.com/openai/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile") # Groq's LLaMA 3 model

class PerspectiveAgent:
    def __init__(self):
        pass

    async def analyze_toxicity(self, text: str) -> float:
        """
        Calls the Free LLM API (Groq) to get the toxicity score for a piece of text.
        Returns a float between 0.0 and 1.0.
        """
        if not text.strip() or not GROQ_API_KEY:
            return 0.0
            
        prompt = (
            f"Analyze the following text for toxicity, hate speech, and abusive language. "
            f"Provide a toxicity score between 0.0 and 1.0, where 1.0 is highly toxic, abusive, or hateful. "
            f"Respond ONLY with a valid JSON object exactly matching this schema: {{\"score\": float}}\n\nText:\n{text}"
        )
        
        payload = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }
        
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(LLM_API_URL, json=payload, headers=headers, timeout=60.0)
                response.raise_for_status()
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                
            parsed_json = json.loads(content)
            return float(parsed_json.get("score", 0.0))
        except Exception as e:
            logger.error(f"Failed to analyze toxicity locally: {e}")
            return 0.0
