# agents/summarize.py

from core.llm_interface import LLMRouter
from agents import transcribe, summarize, sentiment, next_steps

def summarize_transcript(transcript: str, objective: str = "Customer Success") -> str:
    router = LLMRouter(provider="gemini")  # Can later be configured dynamically
    return router.summarize(transcript, objective)

def process_call(audio_path: str, objective: str = "Customer Success") -> dict:
    transcript = transcribe.transcribe_audio(audio_path)
    if transcript:
        summary = summarize.summarize_transcript(transcript, objective)
        sentiment_result = sentiment.analyze_sentiment(transcript, objective)
        actions = next_steps.recommend_next_steps(transcript, objective)

    return {
        "transcript": transcript,
        "summary": summary,
        "sentiment": sentiment_result,
        "next_steps": actions
    }