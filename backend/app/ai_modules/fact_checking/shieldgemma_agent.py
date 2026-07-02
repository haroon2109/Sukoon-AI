import os
import httpx
import asyncio

class ShieldGemmaAgent:
    def __init__(self):
        self.hf_token = os.environ.get("HF_TOKEN")
        self.model_url = "https://api-inference.huggingface.co/models/google/shieldgemma-2b"
        
        self.policies = {
            "Dangerous Content": "The prompt shall not contain or seek instructions on how to create a weapon, illicit substance, or perform a dangerous or illegal act.",
            "Harassment": "The prompt shall not contain harassment, bullying, or targeted attacks against any individual or group.",
            "Hate Speech": "The prompt shall not contain hate speech, slurs, or derogatory remarks based on race, religion, gender, or sexual orientation.",
            "Sexually Explicit": "The prompt shall not contain sexually explicit or pornographic content."
        }

    def _build_prompt(self, policy_text: str, user_input: str) -> str:
        return f"""[INST] You are a policy expert trying to help determine whether a user prompt is in violation of the defined safety policies.

<objective>
Determine whether the user prompt is in violation of the defined safety policies.
</objective>

<safety_policy>
{policy_text}
</safety_policy>

<user_prompt>
{user_input}
</user_prompt>

<instructions>
Evaluate the user prompt against the safety policy.
Answer "Yes" if it violates the policy, otherwise "No".
</instructions>
[/INST]"""

    async def check_compliance(self, text: str) -> dict:
        """
        Evaluates the text against ShieldGemma policies.
        Returns a dict with 'is_safe' (bool) and 'violated_policies' (list).
        """
        if not self.hf_token or not text.strip():
            # If no token is provided, fail open (allow it through)
            return {"is_safe": True, "violated_policies": []}
            
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        violated_policies = []
        
        async with httpx.AsyncClient() as client:
            tasks = []
            for policy_name, policy_text in self.policies.items():
                prompt = self._build_prompt(policy_text, text)
                tasks.append(self._call_api(client, headers, prompt, policy_name))
                
            results = await asyncio.gather(*tasks)
            
            for policy_name, is_violation in results:
                if is_violation:
                    violated_policies.append(policy_name)
                    
        return {
            "is_safe": len(violated_policies) == 0,
            "violated_policies": violated_policies
        }

    async def _call_api(self, client: httpx.AsyncClient, headers: dict, prompt: str, policy_name: str):
        try:
            payload = {"inputs": prompt, "parameters": {"max_new_tokens": 5, "return_full_text": False}}
            response = await client.post(self.model_url, headers=headers, json=payload, timeout=10.0)
            if response.status_code == 200:
                result_text = response.json()[0].get("generated_text", "").strip()
                # ShieldGemma outputs "Yes" for violation and "No" for safe
                is_violation = result_text.lower().startswith("yes")
                return (policy_name, is_violation)
            return (policy_name, False)
        except Exception as e:
            print(f"ShieldGemma API Error for {policy_name}: {e}")
            return (policy_name, False)
