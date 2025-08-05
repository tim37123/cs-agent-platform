from fastapi import APIRouter, File, UploadFile
from pydantic import BaseModel
from core.llm_interface import LLMRouter
from fastapi.responses import JSONResponse
import os
import uuid
import aiofiles

router = APIRouter()

@router.post("/upload-call")
async def upload(file: UploadFile = File(...)):

    if not file.filename or not file.filename.endswith((".mp3", ".wav")):
        return JSONResponse(status_code=400, content={"error": "Invalid file type"})

    UPLOAD_DIR = "data/sample_calls"
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[-1]
    call_id = str(uuid.uuid4())
    save_path = os.path.join(UPLOAD_DIR, f"{call_id}{file_ext}")

    # Save file to disk
    # with open(save_path, "wb") as f:
    #     f.write(await file.read())

    async with aiofiles.open(save_path, "wb") as out_file:
        content = await file.read()  # still async
        await out_file.write(content)

    return {
        "message": "Upload successful",
        "call_id": call_id,
        "file_path": save_path
    }