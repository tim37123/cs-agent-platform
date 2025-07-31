import os
import requests

class Qwen:
    def __init__(self):
        self.api_url = os.getenv("QWEN_API_URL", "http://llm-qwen3:8000")

    def _call(self, prompt, max_new_tokens=256):
        resp = requests.post(
            f"{self.api_url}/v1/completions",
            json={"model": "Qwen/Qwen3-8B", "prompt": prompt, "max_tokens": max_new_tokens},
            timeout=60
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["text"].strip()

    def summarize(self, transcript, objective):
        prompt = f"""
        You are an expert assistant helping with: {objective}
        Summarize the following conversation into 3–5 bullet points including:
        - Key goals
        - Objections or concerns
        - Sentiment and tone
        - Recommended follow-up actions

        Transcript:
        {transcript}
        """
        return self._call(prompt)

    def analyze_sentiment(self, transcript, objective):
        prompt = f"""
        You are a conversation analysis agent focused on: {objective}.
        Determine the overall sentiment of this customer conversation. Choose one word: Positive, Neutral, or Negative.
        
        Transcript:
        {transcript}
        """
        return self._call(prompt)
    
    def next_steps(self, transcript: str, objective: str) -> list[str]:
        prompt = f"""
        You are an expert assistant in: {objective}.
        Based on the conversation below, suggest 2–3 actionable next steps that the user (e.g., a Customer Success Manager) should take.
        Format your response as a list.
        
        Transcript:
        {transcript}
        """
        return self._call(prompt)
