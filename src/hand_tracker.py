import cv2
import mediapipe as mp
import os

class HandTracker:
    def __init__(self, model_path='hand_landmarker.task'):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file '{model_path}' not found!")

        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=model_path),
            running_mode=VisionRunningMode.IMAGE,
            num_hands=1
        )
        self.landmarker = HandLandmarker.create_from_options(options)

    def get_index_tip(self, frame):
        """Tracks index fingertip (Landmark 8) coordinates in real time."""
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        results = self.landmarker.detect(mp_image)

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                index_tip = hand_landmarks[8]  # Landmark 8: Index Fingertip
                return int(index_tip.x * w), int(index_tip.y * h)
                
        return None