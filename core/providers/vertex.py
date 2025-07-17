from vertexai.preview.language_models import TextGenerationModel

class GeminiLLM:
    def __init__(self):
        self.model = TextGenerationModel.from_pretrained("gemini-1.5-flash-preview")

    def summarize(self, transcript: str, objective: str) -> str:
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
        response = self.model.predict(prompt, temperature=0.4, max_output_tokens=512)
        return response.text.strip()

    def analyze_sentiment(self, transcript: str, objective: str) -> str:
        prompt = f"""
        You are a conversation analysis agent focused on: {objective}.
        Determine the overall sentiment of this customer conversation. Choose one word: Positive, Neutral, or Negative.
        
        Transcript:
        {transcript}
        """
        response = self.model.predict(prompt, temperature=0.2, max_output_tokens=10)
        return response.text.strip()

    def next_steps(self, transcript: str, objective: str) -> list[str]:
        prompt = f"""
        You are an expert assistant in: {objective}.
        Based on the conversation below, suggest 2–3 actionable next steps that the user (e.g., a Customer Success Manager) should take.
        Format your response as a list.
        
        Transcript:
        {transcript}
        """
        response = self.model.predict(prompt, temperature=0.5, max_output_tokens=256)
        return [line.strip("-• \n") for line in response.text.strip().splitlines() if line.strip()]