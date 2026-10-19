"""MediaPipe hand tracker factory."""
def create_hand_tracker(max_num_hands=1, detection_confidence=0.5, tracking_confidence=0.5):
    import mediapipe as mp
    return mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=max_num_hands,
        min_detection_confidence=detection_confidence, min_tracking_confidence=tracking_confidence)
