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
