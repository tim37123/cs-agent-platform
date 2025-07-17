from core.llm_interface import LLMRouter

def analyze_sentiment(transcript: str, objective: str = "Customer Success") -> str:
    router = LLMRouter(provider="gemini")
    return router.analyze_sentiment(transcript, objective)
