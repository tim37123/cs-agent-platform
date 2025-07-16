# api/main.py

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import os
import uuid

from agents.transcribe import transcribe_audio

app = FastAPI()

UPLOAD_DIR = "data/sample_calls"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        return{
            "call_id": call_id,
            "transcript": transcript
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})