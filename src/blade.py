import cv2
from collections import deque

class BladeTrail:
    def __init__(self, max_length=10):
        self.points = deque(maxlen=max_length)

    def update(self, point):
        if point:
            self.points.appendleft(point)
        elif len(self.points) > 0:
            self.points.pop()

    def draw(self, frame):
        for i in range(1, len(self.points)):
            thickness = int(12 * (1 - (i / self.points.maxlen)))
            color = (255, 255, int(255 * (1 - (i / self.points.maxlen))))
            if thickness > 0:
                cv2.line(frame, self.points[i - 1], self.points[i], color, thickness)