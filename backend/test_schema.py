import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

config = types.GenerateContentConfig(
    tools=[types.Tool(google_search=types.GoogleSearch())],
    temperature=0.0,
    response_mime_type="application/json",
    response_schema={
        "type": "OBJECT",
        "properties": {
            "verdict": {"type": "STRING", "enum": ["TRUE", "FALSE", "MISLEADING", "TOXIC"]},
            "explanation": {"type": "STRING"}
        },
        "required": ["verdict", "explanation"]
    }
)

try:
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Fact-check this: the sky is blue",
        config=config
    )
    print("SUCCESS!")
    print(response.text)
except Exception as e:
    print("FAILED!")
    print(str(e))
