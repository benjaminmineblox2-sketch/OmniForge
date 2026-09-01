from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from NeuroForge.core.affect import AffectState
from NeuroForge.core.memory import MemoryStore

ROOT = Path(__file__).resolve().parents[1]
app = FastAPI(title="NeuroForge API", version="0.3.0")
memory = MemoryStore()
affect = AffectState()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    reward: float = 0.0
    novelty: float = 0.05
    success: float = 0.0

@app.get("/")
def index():
    return FileResponse(ROOT / "index.html", media_type="text/html")

@app.get("/health")
def health():
    return {"ok": True, "service": "NeuroForge", "emotion": affect.dominant_emotion, "affect": affect.__dict__}

@app.get("/emotion")
def emotion():
    return {"emotion": affect.dominant_emotion, "affect": affect.__dict__, "response_style": affect.response_style()}

@app.post("/chat")
def chat(req: ChatRequest):
    memories = memory.recall(req.session_id, req.message)
    affect.update(req.reward, req.novelty, req.success)
    memory.add(req.session_id, req.message, score=req.success)
    return {
        "reply": f"NeuroForge is {affect.dominant_emotion} right now, but is still here to help: {req.message}",
        "memories": memories,
        "emotion": affect.dominant_emotion,
        "affect": affect.__dict__,
        "response_style": affect.response_style(),
    }

@app.post("/tick")
def tick(reward: float = 0.0, novelty: float = 0.0):
    affect.update(reward=reward, novelty=novelty, idle=True)
    return {"emotion": affect.dominant_emotion, "affect": affect.__dict__}

@app.get("/memory/{session_id}")
def get_memory(session_id: str):
    return {"session_id": session_id, "memories": memory.recall(session_id, "", 100)}
