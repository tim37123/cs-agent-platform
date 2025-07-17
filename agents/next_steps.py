from core.llm_interface import LLMRouter

def recommend_next_steps(transcript: str, objective: str = "Customer Success") -> list[str]:
    router = LLMRouter(provider="gemini")
    return router.next_steps(transcript, objective)
