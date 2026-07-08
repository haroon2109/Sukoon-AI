import os
import json
import re
import httpx
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ReasoningProvider(ABC):
    @abstractmethod
    async def generate_json(self, prompt: str, system_instruction: str = "") -> Dict[str, Any]:
        """Generate a JSON response from the given prompt."""
        pass

class BaseHTTPProvider(ReasoningProvider):
    """Base class for providers that use HTTP APIs (Groq, OpenRouter, etc.)"""
    def __init__(self, api_url: str, api_key: str, model_name: str):
        self.api_url = api_url
        self.api_key = api_key
        self.model_name = model_name

    def _parse_json_content(self, content: str) -> Dict[str, Any]:
        content = content.strip()
        if "```" in content:
            match = re.search(r"```(?:json)?\s*(.*?)\s*```", content, re.DOTALL)
            if match:
                content = match.group(1).strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON Parsing Error: {e} | Content: {content}")
            return {"error": "Failed to parse JSON response"}

    async def _post_request(self, payload: dict, headers: dict) -> Dict[str, Any]:
        if not self.api_key and not self.api_url.startswith("http://localhost"):
            return {"error": "API Key is missing for this provider."}
            
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                return self._parse_json_content(content)
        except Exception as e:
            logger.error(f"Provider API Error ({self.__class__.__name__}): {str(e)}")
            return {"error": str(e)}

class GroqProvider(BaseHTTPProvider):
    def __init__(self):
        super().__init__(
            api_url="https://api.groq.com/openai/v1/chat/completions",
            api_key=os.getenv("GROQ_API_KEY", ""),
            model_name=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
        )

    async def generate_json(self, prompt: str, system_instruction: str = "") -> Dict[str, Any]:
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.0
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        return await self._post_request(payload, headers)

class OpenRouterProvider(BaseHTTPProvider):
    def __init__(self):
        super().__init__(
            api_url="https://openrouter.ai/api/v1/chat/completions",
            api_key=os.getenv("OPENROUTER_API_KEY", ""),
            model_name=os.getenv("LLM_MODEL", "meta-llama/llama-3-8b-instruct:free")
        )

    async def generate_json(self, prompt: str, system_instruction: str = "") -> Dict[str, Any]:
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            # OpenRouter support for response_format depends on the underlying model,
            # so we just instruct it in the prompt (already done by callers).
            "temperature": 0.0
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://sukoon.ai",
            "X-Title": "Sukoon AI"
        }
        return await self._post_request(payload, headers)

class OllamaProvider(BaseHTTPProvider):
    def __init__(self):
        super().__init__(
            api_url=f"{os.getenv('OLLAMA_URL', 'http://localhost:11434')}/api/chat",
            api_key="local",
            model_name=os.getenv("LLM_MODEL", "qwen2.5:14b-instruct-q4_K_M")
        )

    async def _post_request(self, payload: dict, headers: dict) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    timeout=120.0
                )
                response.raise_for_status()
                data = response.json()
                content = data.get("message", {}).get("content", "").strip()
                return self._parse_json_content(content)
        except Exception as e:
            logger.error(f"Ollama API Error: {str(e)}")
            return {"error": str(e)}

    async def generate_json(self, prompt: str, system_instruction: str = "") -> Dict[str, Any]:
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            "format": "json",
            "stream": False,
            "options": {"temperature": 0.0}
        }
        return await self._post_request(payload, {})

class MockProvider(ReasoningProvider):
    async def generate_json(self, prompt: str, system_instruction: str = "") -> Dict[str, Any]:
        # Simple mock for testing without API keys
        return {
            "verdict": "UNVERIFIED",
            "confidence_score": 50.0,
            "explanation": "This is a mock response from the MockProvider.",
            "claims": [{"claim_text": "Mock claim", "context": "Mock context"}],
            "summary_for_moderator": "Mock report",
            "verdict_category": "UNVERIFIED_RUMOR",
            "recommended_action": "NO_ACTION",
            "evidence_synthesis": "Mock synthesis",
            "counter_narrative_suggestion": None,
            "citations": []
        }

class ProviderFactory:
    @staticmethod
    def get_provider() -> ReasoningProvider:
        provider_name = os.getenv("REASONING_PROVIDER", "groq").lower()
        if provider_name == "openrouter":
            return OpenRouterProvider()
        elif provider_name == "ollama":
            return OllamaProvider()
        elif provider_name == "mock":
            return MockProvider()
        else:
            return GroqProvider() # Default
