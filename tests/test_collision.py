from src.collision import point_hits_circle

def test_point_inside_circle(): assert point_hits_circle((2, 2), (0, 0), 4)

def test_point_outside_circle(): assert not point_hits_circle((10, 10), (0, 0), 2)
