from fastapi import FastAPI
from pydantic import BaseModel
from NeuroForge.core.affect import AffectState
from NeuroForge.core.memory import MemoryStore

app = FastAPI(title="NeuroForge API", version="0.1.0")
memory = MemoryStore()
affect = AffectState()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

@app.get("/health")
def health():
    return {"ok": True, "service": "NeuroForge", "affect": affect.__dict__}

@app.post("/chat")
def chat(req: ChatRequest):
    memories = memory.recall(req.session_id, req.message)
    memory.add(req.session_id, req.message)
    affect.update(0.01, novelty=0.1 if not memories else 0.0)
    return {
        "reply": f"NeuroForge received: {req.message}",
        "memories": memories,
        "affect": affect.__dict__,
    }

@app.get("/memory/{session_id}")
def get_memory(session_id: str):
    return {"session_id": session_id, "memories": memory.recall(session_id, "", 100)}
