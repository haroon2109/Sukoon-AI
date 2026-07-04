from ..agents.supervisor import SupervisorAgent

supervisor = SupervisorAgent()

def process_text_claim(text: str, is_deep: bool = False) -> dict:
    """Processes a text claim using the Supervisor Agent."""
    # We can pass is_deep to user_context if needed
    result = supervisor.process_request(text, user_context={"is_deep": is_deep})
    return result
