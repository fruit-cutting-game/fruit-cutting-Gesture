import math

class MotionAnalyzer:
    def __init__(self, speed_threshold=15.0):
        self.prev_point = None
        self.speed_threshold = speed_threshold  # Minimum distance per frame to count as a cut

    def calculate_speed_and_distance(self, current_point):
        """Calculates movement distance and speed between current and previous frame points."""
        if current_point is None or self.prev_point is None:
            self.prev_point = current_point
            return 0.0, False

        # Calculate Euclidean distance: sqrt((x2 - x1)^2 + (y2 - y1)^2)
        dx = current_point[0] - self.prev_point[0]
        dy = current_point[1] - self.prev_point[1]
        distance = math.hypot(dx, dy)

        # Distance moved per frame acts as speed
        speed = distance 
        is_cutting = speed >= self.speed_threshold

        self.prev_point = current_point
        return speed, is_cutting