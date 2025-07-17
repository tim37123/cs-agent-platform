from typing import Literal
def transcribe_audio(file_path: str, provider: Literal["whisper", "gcp"] = "whisper") -> str:
    if provider == "whisper":
        return _transcribe_with_whisper(file_path)
    elif provider == "gcp":
        raise NotImplementedError("GCP transcription is not implemented yet")
    else:
        raise ValueError(f"Invalid provider: {provider}")

def _transcribe_with_whisper(file_path: str) -> str:
    import whisper
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    text = result["text"]
    if isinstance(text, list):
        text = " ".join(str(segment) for segment in text)
    return text
