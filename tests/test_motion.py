from src.motion_analyzer import distance, speed

def test_distance(): assert distance((0, 0), (3, 4)) == 5

def test_speed(): assert speed((0, 0), (3, 4), 1) == 5
