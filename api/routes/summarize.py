from fastapi import APIRouter
from pydantic import BaseModel
from core.llm_interface import LLMRouter
import openai

router = APIRouter()

class SummarizeRequest(BaseModel):
    transcript: str

class SummarizeResponse(BaseModel):
    summary: str

@router.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    llm = LLMRouter(provider="qwen")
    summary = llm.summarize(request.transcript)
    return {"summary": summary}