import cv2
from collections import deque

class BladeTrail:
    def __init__(self, max_length=10):
        self.points = deque(maxlen=max_length)

    def update(self, point, is_cutting=True):
        """Adds points to trail when cutting, fades out when slow or stopped."""
        if point and is_cutting:
            self.points.appendleft(point)
        elif len(self.points) > 0:
            self.points.pop()  # Fade trail out smoothly when speed drops below threshold

    def draw(self, frame):
        """Draws virtual blade trail on screen."""
        for i in range(1, len(self.points)):
            thickness = int(12 * (1 - (i / self.points.maxlen)))
            color = (255, 255, int(255 * (1 - (i / self.points.maxlen))))
            
            if thickness > 0:
                cv2.line(frame, self.points[i - 1], self.points[i], color, thickness)