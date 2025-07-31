from fastapi import APIRouter
from pydantic import BaseModel
from core.llm_interface import LLMRouter

router = APIRouter()

class OrchestrateRequest(BaseModel):
    transcript: str
    objective: str

class OrchestrateResponse(BaseModel):
    summary: str
    sentiment: str
    next_steps: list[str]

@router.post("/orchestrate", response_model=OrchestrateResponse)
def orchestrate(request: OrchestrateRequest):
    llm = LLMRouter(provider="gemini")
    summary = llm.summarize(request.transcript, request.objective)
    sentiment = llm.analyze_sentiment(request.transcript, request.objective)
    next_steps = llm.next_steps(request.transcript, request.objective)
    return {
        "summary": summary,
        "sentiment": sentiment,
        "next_steps": next_steps
    }
