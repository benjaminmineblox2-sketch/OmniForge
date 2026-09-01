import json
from pathlib import Path
from typing import Any

class MemoryStore:
    def __init__(self, path: str = "data/memory.json", max_items: int = 10000):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.max_items = max_items
        self.items: list[dict[str, Any]] = self._load()

    def _load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []

    def add(self, session_id: str, text: str, score: float = 0.0) -> None:
        self.items.append({"session_id": session_id, "text": text, "score": score})
        self.items = self.items[-self.max_items:]
        self.path.write_text(json.dumps(self.items, ensure_ascii=False, indent=2), encoding="utf-8")

    def recall(self, session_id: str, query: str, k: int = 8) -> list[str]:
        words = set(query.lower().split())
        candidates = [x for x in self.items if x["session_id"] == session_id]
        ranked = sorted(candidates, key=lambda x: len(words & set(x["text"].lower().split())) + x.get("score", 0), reverse=True)
        return [x["text"] for x in ranked[:k]]
