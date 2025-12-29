import mediapipe as mp
import cv2
import time


class PostureDetector:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.baseline_distance = None
        self.last_bad_time = 0

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(rgb)

        if not result.pose_landmarks:
            return None

        lm = result.pose_landmarks.landmark

        left = lm[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
        right = lm[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
        nose = lm[mp.solutions.pose.PoseLandmark.NOSE]

        shoulder_y = (left.y + right.y) / 2
        chin_y = nose.y + (shoulder_y - nose.y) * 0.55

        distance = shoulder_y - chin_y

        if self.baseline_distance is None:
            self.baseline_distance = distance
            return "calibrating"

        bad = distance < self.baseline_distance - 0.035
        return "bad" if bad else "good"
