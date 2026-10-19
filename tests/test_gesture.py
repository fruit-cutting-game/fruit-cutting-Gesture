from src.gesture_detector import is_cut

def test_fast_long_movement_is_cut(): assert is_cut((0, 0), (100, 0), 0.1)

def test_slow_movement_is_not_cut(): assert not is_cut((0, 0), (1, 0), 1)
