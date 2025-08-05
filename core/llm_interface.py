# core/llm_interface.py
import json, os
from typing import Literal
from openai import OpenAI

def load_prompts(file_name):
    file_path = os.path.join(os.path.dirname(__file__), file_name)  # Get the path of the current directory
    with open(file_path, 'r') as file:
        return json.load(file)

class LLMRouter:
    def __init__(self, provider: Literal["gemini", "openai", "qwen"] = "qwen"):
        self.prompts = load_prompts("prompts.json")
        self.provider = provider
        if provider == "qwen":
            print("Using Qwen LLM provider")
            # if on local server
            self.api_base = "http://192.168.1.144:8080/v1"
            # if on tailscale use this 
            # self.api_base = "http://100.71.241.119:8080/v1"
            self.api_key = "sk-0000"  # dummy key
            
        else:
            raise NotImplementedError(f"LLM provider '{provider}' not yet supported.")

    def summarize(self, transcript: str) -> str:
        summ_prompt = self.prompts["summarize_call"]
        client = OpenAI(base_url=self.api_base, api_key=self.api_key)

        return  client.chat.completions.create(
            model=self.provider,
            messages=[
                {"role": "system", "content": summ_prompt["system"]},
                {"role": "user", "content": summ_prompt["user"] + "\n\n" + transcript}
            ]
        ).choices[0].message.content

    def analyze_sentiment(self, transcript: str) -> str:
        summ_prompt = next((p for p in self.prompts["prompts"] if p["scenario"] == "analyze_sentiment"), None)
        # return self.llm.analyze_sentiment(transcript)

    def next_steps(self, transcript: str) -> list[str]:
        summ_prompt = next((p for p in self.prompts["prompts"] if p["scenario"] == "transcribe_audio"), None)
        # return self.llm.next_steps(transcript)
