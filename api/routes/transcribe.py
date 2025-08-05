from fastapi import APIRouter, File, UploadFile
# from pydantic import BaseModel
import os
# from core.llm_interface import LLMRouter
from fastapi.responses import JSONResponse
from fastapi.concurrency import run_in_threadpool
import uuid
from storage.db import SessionLocal
from agents.transcribe import transcribe_audio
from models.call import Call
from sqlalchemy.exc import SQLAlchemyError
import aiofiles

router = APIRouter()


@router.post("/transcribe-call")
async def transcribe(file: UploadFile = File(...)):

    if not file.filename or not file.filename.endswith((".mp3", ".wav")):
        return JSONResponse(status_code=400, content={"error": "Invalid file type"})

    UPLOAD_DIR = "data/sample_calls"
    os.makedirs(UPLOAD_DIR, exist_ok=True)


    file_ext = os.path.splitext(file.filename)[-1]
    call_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{call_id}{file_ext}")

    # with open(save_path, "wb") as f:
    #     f.write(await file.read())

    async with aiofiles.open(save_path, "wb") as f:
        content = await file.read()
        await f.write(content)
    
    try:
        # transcript = transcribe_audio(save_path, provider="whisper")
        transcript = await run_in_threadpool(transcribe_audio, save_path, provider="whisper")
        db = SessionLocal()
        db_call = Call(
            call_id=call_id,
            filename=file.filename,
            transcript=transcript
        )

        db.add(db_call)
        db.commit()
        db.refresh(db_call)
        
        return{
            "call_id": call_id,
            "transcript": transcript
        }
    
    except SQLAlchemyError as db_error:
        return JSONResponse(status_code=500, content={"error": f"DB error: {str(db_error)}"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})