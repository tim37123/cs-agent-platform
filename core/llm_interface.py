# core/llm_interface.py

from typing import Literal
# from core.providers.vertex import GeminiLLM
from core.providers.qwen import Qwen

class LLMRouter:
    def __init__(self, provider: Literal["gemini", "openai", "qwen"] = "qwen"):
        if provider == "qwen":
            self.llm = Qwen()
        else:
            raise NotImplementedError(f"LLM provider '{provider}' not yet supported.")

    def summarize(self, transcript: str, objective: str) -> str:
        return self.llm.summarize(transcript, objective)

    def analyze_sentiment(self, transcript: str, objective: str) -> str:
        return self.llm.analyze_sentiment(transcript, objective)

    def next_steps(self, transcript: str, objective: str) -> list[str]:
        return self.llm.next_steps(transcript, objective)
