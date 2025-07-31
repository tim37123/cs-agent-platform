# api/main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from api.routes import orchestrator, summarize
import os
import uuid
from utils.logger import logger
from storage.startup import initialize_database
from agents.transcribe import transcribe_audio
from models.call import Call
from storage.db import SessionLocal
from sqlalchemy.exc import SQLAlchemyError


app = FastAPI()


UPLOAD_DIR = "data/sample_calls"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
def on_startup():
    logger.info("🚀 Starting up...")
    initialize_database()

app.include_router(orchestrator.router)
app.include_router(summarize.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/upload-call")
async def upload_call(file: UploadFile = File(...)):
    # Check file extension
    if not file.filename or not file.filename.endswith((".mp3", ".wav")):
        return JSONResponse(status_code=400, content={"error": "Invalid file type"})

    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[-1]
    call_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{call_id}{file_ext}")

    # Save file to disk
    with open(save_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Upload successful",
        "call_id": call_id,
        "file_path": save_path
    }

@app.post("/transcribe-call")
async def transcribe_call(file: UploadFile = File(...)):
    if not file.filename or file.filename.endswith((".mp3", ".wav")):
        return JSONResponse(status_code=400, content={"error": "Invalid file type"})
    
    file_ext = os.path.splitext(file.filename)[-1]
    call_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{call_id}{file_ext}")

    with open(save_path, "wb") as f:
        f.write(await file.read())
    
    try:
        transcript = transcribe_audio(save_path, provider="whisper")
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