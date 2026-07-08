import json
import re
import os
import logging
from app.providers.reasoning_provider import ProviderFactory

logger = logging.getLogger(__name__)

class FreeLLMClient:
    def __init__(self):
        pass

    def generate(self, prompt: str) -> str:
        """
        Synchronous wrapper around the async ProviderFactory.
        Used for legacy compatibility.
        """
        import asyncio
        
        async def _run():
            provider = ProviderFactory.get_provider()
            # generate_json returns a dict, but legacy generate returns a string.
            # We'll just ask for JSON and stringify it, or use the raw generate if we had one.
            # Since ReasoningProvider only has generate_json right now, we wrap it.
            res = await provider.generate_json(prompt, system_instruction="You are a helpful AI assistant.")
            return json.dumps(res)
            
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
            return loop.run_until_complete(_run())
        except Exception as e:
            logger.error(f"FreeLLMClient generate error: {e}")
            return "{}"

    def analyze_media(self, file_path: str, mime_type: str, context: str = "") -> dict:
        """
        Analyzes media using the Free LLM (Groq) with OCR/extracted context.
        Groq doesn't natively support image vision models yet, so we rely entirely on the extracted text context.
        """
        prompt = "Please analyze this media file carefully based on the extracted text context."
        if context:
            prompt += f"\n\nContext extracted from the media (OCR/Transcription):\n{context}"
        else:
            prompt += "\n\nNo text could be extracted from the media."
            
        return self.generate(prompt)

llm_client = FreeLLMClient()
