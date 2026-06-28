from ..ai_modules.agents.evaluation_agent import evaluation_agent

def process_text_claim(text: str, is_deep: bool = False) -> dict:
    """Processes a text claim using the Intelligent Evaluation Engine."""
    if is_deep:
        result = evaluation_agent.deep_evaluate(text)
    else:
        result = evaluation_agent.evaluate(text)
    # Add any additional structuring if needed
    return result
