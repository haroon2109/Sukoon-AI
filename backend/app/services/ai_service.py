import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load local environment variables (.env)
load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "arenagrid")
REGION = os.getenv("GCP_REGION", "us-central1")

# 1. Initialize the modern Google Gen AI Client pointing to Vertex AI
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# 2. Define the exact persona for Sukoon AI
SUKOON_SYSTEM_INSTRUCTION = (
    "You are the core evaluation intelligence of Sukoon AI. Your sole mandate is to foster community peace "
    "by fact-checking claims and identifying incitement to hatred, violence, or severe community division. "
    "Analyze the input accurately and provide a structured breakdown."
)

async def evaluate_text_content(user_text: str) -> str:
    """
    Sends raw user text or scraped article content to Gemini 2.5 Flash 
    grounded by our specific peace-keeping system guidelines.
    """
    try:
        # Configure the structural guardrails for the model
        config = types.GenerateContentConfig(
            system_instruction=[SUKOON_SYSTEM_INSTRUCTION],
            temperature=0.2, # Lower temperature makes the model deterministic and less prone to random flareups
        )
        
        # We use gemini-2.5-flash as it is lightning fast and cost-efficient for an MVP
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze this content for peace validation and factual truth: {user_text}",
            config=config,
        )
        
        return response.text

    except Exception as e:
        return f"AI Processing Error: {str(e)}"
