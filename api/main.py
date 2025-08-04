# api/main.py

from fastapi import FastAPI
from api.routes import orchestrator, summarize, upload, transcribe
from utils.logger import logger
from storage.startup import initialize_database

app = FastAPI()

@app.on_event("startup")
def on_startup():
    logger.info("🚀 Starting up...")
    initialize_database()

app.include_router(orchestrator.router)
app.include_router(summarize.router)
app.include_router(upload.router)
app.include_router(transcribe.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}