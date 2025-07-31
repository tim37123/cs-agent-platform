from fastapi import APIRouter
from pydantic import BaseModel
from core.llm_interface import LLMRouter

router = APIRouter()

class SummarizeRequest(BaseModel):
    transcript: str
    objective: str

class SummarizeResponse(BaseModel):
    summary: str

@router.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    llm = LLMRouter(provider="gemini")
    summary = llm.summarize(request.transcript, request.objective)
    return {"summary": summary}
