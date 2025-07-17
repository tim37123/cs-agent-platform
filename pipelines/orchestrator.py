# agents/summarize.py

from core.llm_interface import LLMRouter

def summarize_transcript(transcript: str, objective: str = "Customer Success") -> str:
    router = LLMRouter(provider="gemini")  # Can later be configured dynamically
    return router.summarize(transcript, objective)
