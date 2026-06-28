from pydantic import BaseModel, Field

class PeaceResponseResult(BaseModel):
    peace_message: str = Field(..., description="A calming, empathetic, and factual message to de-escalate panic")

class PeaceResponseAgent:
    """
    Agent responsible for synthesizing the results from the NLP pipeline, 
    risk scores, and context verifier to generate a calm, objective, and empathetic response.
    """
    def __init__(self, model_name: str = "gpt-4o"):
        self.model_name = model_name

    async def run(self, verdict: str, matched_context: str, risk_score: float) -> PeaceResponseResult:
        """
        Generates the Peace Message based on the severity of the claim and the final verdict.
        Uses a system prompt tuned for extreme empathy and de-escalation.
        """
        print(f"[PeaceResponseAgent] Generating peace response for verdict: {verdict} (Risk: {risk_score})")
        
        # In production: Construct a prompt injecting the verdict, context, and risk score.
        
        # Mocking the response for MVP architecture
        message = "Take a deep breath. This information is outdated. You and your family are safe to go about your normal routines today."
        if verdict == "true" and risk_score > 0.7:
            message = "While this claim is true, local authorities are already handling the situation. Please remain calm and rely only on official broadcasts."
            
        return PeaceResponseResult(peace_message=message)
