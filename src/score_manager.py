"""Score and combo tracking helper."""
class ScoreManager:
    def __init__(self): self.score = 0; self.combo = 0
    def add_points(self, points): self.score += points; self.combo += 1; return self.score
    def reset_combo(self): self.combo = 0
