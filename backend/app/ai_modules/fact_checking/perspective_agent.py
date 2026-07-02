import os
import httpx

class PerspectiveAgent:
    def __init__(self):
        # Fallback to GEMINI_API_KEY if PERSPECTIVE_API_KEY isn't explicitly set
        self.api_key = os.environ.get("PERSPECTIVE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={self.api_key}"

    async def analyze_toxicity(self, text: str) -> float:
        """
        Calls the Perspective API to get the toxicity score for a piece of text.
        Returns a float between 0.0 and 1.0. Returns 0.0 if the call fails or key is missing.
        """
        if not self.api_key or not text.strip():
            return 0.0
            
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}}
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.url, json=payload, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
                else:
                    print(f"Perspective API Error: {response.status_code} - {response.text}")
                    return 0.0
        except Exception as e:
            print(f"Failed to connect to Perspective API: {e}")
            return 0.0
