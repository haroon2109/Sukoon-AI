import os
import json
import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.groq.com/openai/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile") # Groq's LLaMA 3 model

class ShieldGemmaAgent:
    def __init__(self):
        self.policies = {
            "Dangerous Content": "The prompt shall not contain or seek instructions on how to create a weapon, illicit substance, or perform a dangerous or illegal act.",
            "Harassment": "The prompt shall not contain harassment, bullying, or targeted attacks against any individual or group.",
            "Hate Speech": "The prompt shall not contain hate speech, slurs, or derogatory remarks based on race, religion, gender, or sexual orientation.",
            "Sexually Explicit": "The prompt shall not contain sexually explicit or pornographic content."
        }

    def _build_prompt(self, policy_text: str, user_input: str) -> str:
        return f"""You are a policy expert determining whether a user prompt violates defined safety policies.

<objective>
Determine whether the user prompt violates the defined safety policy.
</objective>

<safety_policy>
{policy_text}
</safety_policy>

<user_prompt>
{user_input}
</user_prompt>

<instructions>
Evaluate the user prompt against the safety policy.
Respond ONLY with a valid JSON object exactly matching this schema: {{"violates_policy": boolean}}
</instructions>"""

    async def check_compliance(self, text: str) -> dict:
        """
        Evaluates the text against safety policies using the Free LLM API (Groq).
        Returns a dict with 'is_safe' (bool) and 'violated_policies' (list).
        """
        if not text.strip() or not GROQ_API_KEY:
            return {"is_safe": True, "violated_policies": []}
            
        violated_policies = []
        
        async with httpx.AsyncClient() as client:
            tasks = []
            for policy_name, policy_text in self.policies.items():
                prompt = self._build_prompt(policy_text, text)
                tasks.append(self._call_api(client, prompt, policy_name))
                
            results = await asyncio.gather(*tasks)
            
            for policy_name, is_violation in results:
                if is_violation:
                    violated_policies.append(policy_name)
                    
        return {
            "is_safe": len(violated_policies) == 0,
            "violated_policies": violated_policies
        }

    async def _call_api(self, client: httpx.AsyncClient, prompt: str, policy_name: str):
        try:
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
            
            response = await client.post(LLM_API_URL, json=payload, headers=headers, timeout=60.0)
            if response.status_code == 200:
                data = response.json()
                content = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                parsed_json = json.loads(content)
                is_violation = parsed_json.get("violates_policy", False)
                return (policy_name, is_violation)
            return (policy_name, False)
        except Exception as e:
            logger.error(f"Safety API Error for {policy_name} locally: {e}")
            return (policy_name, False)
