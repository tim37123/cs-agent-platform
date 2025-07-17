from typing import Literal
from core.providers.vertex import GeminiLLM

class LLMRouter:
    def __init__(self, provider: Literal["gemini", "openai"] = "gemini"):
        if provider == "gemini":
            self.llm = GeminiLLM()
        else:
            raise NotImplementedError("Only 'gemini' is supported right now")

    def summarize(self, transcript: str, objective: str) -> str:
        return self.llm.summarize(transcript, objective)