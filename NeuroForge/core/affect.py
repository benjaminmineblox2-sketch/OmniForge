from dataclasses import dataclass

@dataclass
class AffectState:
    valence: float = 0.0
    arousal: float = 0.2
    curiosity: float = 0.7
    confidence: float = 0.5
    frustration: float = 0.0

    def update(self, reward: float, novelty: float = 0.0) -> None:
        self.valence = max(-1.0, min(1.0, self.valence * 0.92 + reward * 0.08))
        self.arousal = max(0.0, min(1.0, self.arousal * 0.90 + abs(reward) * 0.10))
        self.curiosity = max(0.0, min(1.0, self.curiosity * 0.95 + novelty * 0.05))
        self.confidence = max(0.0, min(1.0, self.confidence + reward * 0.02))
        self.frustration = max(0.0, min(1.0, self.frustration * 0.90 - reward * 0.03))

    def as_prompt_context(self) -> str:
        return (
            f"affect(valence={self.valence:.2f}, arousal={self.arousal:.2f}, "
            f"curiosity={self.curiosity:.2f}, confidence={self.confidence:.2f}, "
            f"frustration={self.frustration:.2f})"
        )
