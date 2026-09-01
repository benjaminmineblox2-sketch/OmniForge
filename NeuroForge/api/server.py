from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from NeuroForge.core.affect import AffectState
from NeuroForge.core.memory import MemoryStore

app = FastAPI(title="NeuroForge API", version="0.3.0")

memory = MemoryStore()
affect = AffectState()

BASE_DIR = Path(__file__).resolve().parent.parent
INDEX_FILE = BASE_DIR / "index.html"


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"
    reward: float = 0.0
    novelty: float = 0.05
    success: float = 0.0


@app.get("/", include_in_schema=False)
def home():
    """Serve the NeuroForge browser interface."""
    return FileResponse(INDEX_FILE, media_type="text/html")


@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "NeuroForge",
        "emotion": affect.dominant_emotion,
        "affect": affect.__dict__,
    }


@app.get("/emotion")
def emotion():
    return {
        "emotion": affect.dominant_emotion,
        "affect": affect.__dict__,
        "response_style": affect.response_style(),
    }


@app.post("/chat")
def chat(req: ChatRequest):
    memories = memory.recall(req.session_id, req.message)

    affect.update(
        req.reward,
        req.novelty,
        req.success,
    )

    memory.add(
        req.session_id,
        req.message,
        score=req.success,
    )

    # Temporary response until the trained language model is connected.
    reply = (
        f"I'm currently feeling {affect.dominant_emotion}, "
        f"but I'm still focused on helping you. "
        f"You said: {req.message}"
    )

    return {
        "reply": reply,
        "memories": memories,
        "emotion": affect.dominant_emotion,
        "affect": affect.__dict__,
        "response_style": affect.response_style(),
    }


@app.post("/tick")
def tick(reward: float = 0.0, novelty: float = 0.0):
    affect.update(
        reward=reward,
        novelty=novelty,
        idle=True,
    )

    return {
        "emotion": affect.dominant_emotion,
        "affect": affect.__dict__,
    }


@app.get("/memory/{session_id}")
def get_memory(session_id: str):
    return {
        "session_id": session_id,
        "memories": memory.recall(session_id, "", 100),
    }
