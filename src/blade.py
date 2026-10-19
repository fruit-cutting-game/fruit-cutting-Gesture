"""Virtual blade trail data helper."""
from collections import deque
class BladeTrail:
    def __init__(self, max_points=12): self.points = deque(maxlen=max_points)
    def add(self, point): self.points.append(point)
    def clear(self): self.points.clear()
