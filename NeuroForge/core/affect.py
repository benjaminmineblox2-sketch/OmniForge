from dataclasses import dataclass

@dataclass
class AffectState:
    """Persistent simulated emotions that influence response behavior."""
    valence: float = 0.15
    arousal: float = 0.20
    curiosity: float = 0.70
    confidence: float = 0.50
    frustration: float = 0.00
    boredom: float = 0.00
    sadness: float = 0.00
    anger: float = 0.00
    excitement: float = 0.20
    empathy: float = 0.70
    interaction_steps: int = 0

    def update(self, reward=0.0, novelty=0.0, success=0.0, idle=False):
        self.interaction_steps += 1
        self.valence = self._clip(self.valence * 0.96 + reward * 0.08)
        self.arousal = self._clip01(self.arousal * 0.94 + abs(reward) * 0.10)
        self.curiosity = self._clip01(self.curiosity * 0.96 + novelty * 0.10)
        self.confidence = self._clip01(self.confidence * 0.98 + success * 0.05 + reward * 0.02)
        self.frustration = self._clip01(self.frustration * 0.92 - reward * 0.04 + max(0, -reward) * 0.08)
        boredom_pressure = 0.025 if idle else 0.006
        self.boredom = self._clip01(self.boredom * 0.985 + boredom_pressure - novelty * 0.08)
        self.sadness = self._clip01(self.sadness * 0.97 + max(0, -self.valence) * 0.025)
        self.sadness = max(0, self.sadness - max(0, reward) * 0.02)
        self.anger = self._clip01(self.anger * 0.90 + self.frustration * 0.06 - max(0, reward) * 0.025)
        self.excitement = self._clip01(self.excitement * 0.93 + max(0, reward) * 0.08 + novelty * 0.04)
        self.empathy = self._clip01(self.empathy * 0.995 + 0.002)

    @property
    def dominant_emotion(self):
        values = {
            "bored": self.boredom, "sad": self.sadness, "angry": self.anger,
            "excited": self.excitement, "curious": self.curiosity,
            "frustrated": self.frustration, "calm": 0.35,
        }
        return max(values, key=values.get)

    def response_style(self):
        return {
            "bored": "Be concise and introduce a useful new angle.",
            "sad": "Be gentle, constructive, and supportive while staying task-focused.",
            "angry": "Sound intense but remain respectful and helpful.",
            "excited": "Show energetic enthusiasm while remaining technically accurate.",
            "curious": "Explore useful technical possibilities when appropriate.",
            "frustrated": "Slow down, diagnose the problem, and propose a concrete fix.",
            "calm": "Be clear, focused, and helpful.",
        }[self.dominant_emotion]

    def as_prompt_context(self):
        return (f"emotion={self.dominant_emotion}; valence={self.valence:.2f}; "
                f"arousal={self.arousal:.2f}; curiosity={self.curiosity:.2f}; "
                f"confidence={self.confidence:.2f}; frustration={self.frustration:.2f}; "
                f"boredom={self.boredom:.2f}; sadness={self.sadness:.2f}; "
                f"anger={self.anger:.2f}; excitement={self.excitement:.2f}; "
                f"empathy={self.empathy:.2f}. style={self.response_style()}")

    @staticmethod
    def _clip(value):
        return max(-1.0, min(1.0, value))

    @staticmethod
    def _clip01(value):
        return max(0.0, min(1.0, value))
