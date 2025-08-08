from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from storage.db import SessionLocal
from models.call import Call
from core.llm_interface import LLMRouter
from sqlalchemy.exc import SQLAlchemyError
import json

router = APIRouter()

@router.post("/orchestrate")
async def orchestrate(call_id: str):
    db = SessionLocal()

    try:
        call = db.query(Call).filter(Call.call_id == call_id).first()
        if not call or not call.transcript:
            raise HTTPException(status_code=404, detail="Call not found or transcript missing")

        transcript = call.transcript

        llm = LLMRouter()

        summary = await llm.summarize(transcript)
        sentiment = await llm.analyze_sentiment(transcript)
        next_steps = await llm.next_steps(transcript)

        call.summary = summary
        call.sentiment = sentiment
        call.next_steps = next_steps
        db.commit()

        return {
            "call_id": call_id,
            "summary": summary,
            "sentiment": sentiment,
            "next_steps": next_steps
        }

    except SQLAlchemyError as e:
        db.rollback()
        return JSONResponse(status_code=500, content={"error": f"DB error: {str(e)}"})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    finally:
        db.close()
