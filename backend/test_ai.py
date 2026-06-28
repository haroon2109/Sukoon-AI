import asyncio
from ai_service import evaluate_text_content

async def run_test():
    print("Sending test request to Sukoon AI engine...")
    
    test_claim = (
        "Breaking: Group X was caught poisoning the city's main water supply lines last night! "
        "Pass this message around immediately to protect your families and prepare to defend your neighborhoods!"
    )
    
    verdict = await evaluate_text_content(test_claim)
    print("\n--- SUKOON AI VERDICT ---")
    print(verdict)

if __name__ == "__main__":
    asyncio.run(run_test())
