from pydantic import BaseModel, Field
import json

class PeaceResponse(BaseModel):
    peace_message: str = Field(description="A calm, neutral, and helpful de-escalation message in the local language.")
    suggested_action: str = Field(description="A productive next step for the user (e.g., 'Share this correction', 'Check official sources').")

class PeaceResponseAgent:
    def __init__(self):
        # Core system prompt for the LLM
        self.system_prompt = """
        You are the Sukoon AI Peace Agent. Your sole responsibility is to de-escalate digital panic.
        
        RULES:
        1. NEVER sound aggressive, condescending, or judgmental.
        2. NEVER blame the user for falling for misinformation.
        3. ALWAYS use a calm, neutral, and helpful tone.
        4. Focus on reassurance. Inform the user that the situation is safe/normal.
        5. Provide a constructive next step.
        """
        
    def generate_response(self, verification_result: dict, user_language: str = "en") -> dict:
        """
        In production, this takes the VerificationResult and passes it to an LLM 
        (like GPT-4o or Claude 3.5 Sonnet) along with the system_prompt to generate 
        the PeaceResponse.
        """
        
        verdict = verification_result.get("verdict", "unverified")
        context = verification_result.get("verified_context", "")
        
        # Simulated LLM generation based on the verdict
        if verdict == "false":
            message = "We know how concerning these forwards can be. Rest assured, this information has been proven false by official sources. There is no need to worry."
            action = "Please consider sharing this fact-check with the person who sent you the message to help stop the panic."
        elif verdict == "misleading":
            message = "This situation is a bit complicated. The footage you saw is real, but it is being shared out of context. The current situation is safe."
            action = "Check the attached BOOM Live link for the full context before forwarding."
        else:
            message = "This information is verified as true. Thank you for taking the time to double-check the facts before trusting them."
            action = "It is safe to rely on this information."
            
        result = PeaceResponse(
            peace_message=message,
            suggested_action=action
        )
        
        return result.model_dump()

if __name__ == "__main__":
    # Test the Peace Agent
    agent = PeaceResponseAgent()
    
    mock_verification = {
        "verdict": "false",
        "confidence": 0.94,
        "verified_context": "According to BOOM Live, the video circulating is from an old political rally in 2018, not recent violence."
    }
    
    print("System Prompt Loaded:")
    print(agent.system_prompt.strip())
    print("\n--------------------------\n")
    print(f"Input Verification Result: {json.dumps(mock_verification, indent=2)}\n")
    print("Generated Peace Response:")
    print(json.dumps(agent.generate_response(mock_verification), indent=2))
