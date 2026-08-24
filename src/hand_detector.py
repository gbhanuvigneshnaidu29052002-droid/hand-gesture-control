import math
import cv2
import mediapipe as mp

class HandDetector:
    """
    Detects hand landmarks using MediaPipe and provides utility functions
    like extracting landmark positions, checking finger states, and distance measuring.
    """

    def __init__(self, max_hands=1, model_complexity=0, detection_conf=0.5, tracking_conf=0.5):
        # Initialize MediaPipe Hands module
        self.mp_hands = mp.solutions.hands

        # Create hand detection object (model_complexity=0 for 30+ FPS CPU execution)
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            model_complexity=model_complexity,
            min_detection_confidence=detection_conf,
            min_tracking_confidence=tracking_conf
        )

        # Drawing utilities for visualization
        self.mp_draw = mp.solutions.drawing_utils

        # Store landmarks
        self.landmarks = []
        self.results = None

    def find_hands(self, frame, draw=True):
        """
        Detect hands and optionally draw landmarks on frame
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        # Draw landmarks if detected
        if self.results and self.results.multi_hand_landmarks and draw:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )

        return frame

    def get_landmarks(self, frame):
        """
        Extract (id, x, y) positions of hand landmarks
        """
        self.landmarks = []

        if not self.results or not self.results.multi_hand_landmarks:
            return []

        h, w, _ = frame.shape
        hand = self.results.multi_hand_landmarks[0]

        for idx, lm in enumerate(hand.landmark):
            self.landmarks.append((idx, int(lm.x * w), int(lm.y * h)))

        return self.landmarks

    def fingers_up(self):
        """
        Returns list of booleans representing which fingers are up
        [Thumb, Index, Middle, Ring, Pinky]
        """
        if not self.landmarks:
            return [False] * 5

        fingers = []

        # Thumb (horizontal comparison)
        fingers.append(self.landmarks[4][1] > self.landmarks[3][1])

        # Other fingers (vertical comparison)
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]

        for tip, pip in zip(tips, pips):
            fingers.append(self.landmarks[tip][2] < self.landmarks[pip][2])

        return fingers

    def find_distance(self, p1, p2, frame=None, draw=True):
        """
        Calculate Euclidean distance between landmark points p1 and p2
        """
        if not self.landmarks or len(self.landmarks) <= max(p1, p2):
            return 0, frame, []

        x1, y1 = self.landmarks[p1][1], self.landmarks[p1][2]
        x2, y2 = self.landmarks[p2][1], self.landmarks[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        length = math.hypot(x2 - x1, y2 - y1)

        if draw and frame is not None:
            cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv2.circle(frame, (x1, y1), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 8, (255, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), 8, (0, 0, 255), cv2.FILLED)

        return length, frame, [x1, y1, x2, y2, cx, cy]