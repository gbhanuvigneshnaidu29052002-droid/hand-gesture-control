from collections import deque, Counter
import config

class GestureController:
    """
    Maps finger states and spatial distance to specific UI gestures with temporal stabilization.
    """

    def __init__(self, buffer_size=config.BUFFER_SIZE):
        self.history = deque(maxlen=buffer_size)
        self.last_stable_gesture = "NONE"

    def _raw_detect(self, fingers, pinch_distance):
        thumb, index, middle, ring, pinky = fingers[0], fingers[1], fingers[2], fingers[3], fingers[4]

        # 1. DRAG: Strictly Pinching Thumb and Index finger together (distance < PINCH_THRESHOLD)
        if pinch_distance < config.PINCH_THRESHOLD:
            return "DRAG"

        # 2. POINT: Only Index finger up (ignore thumb position so pointing never triggers drag)
        if index and not middle and not ring and not pinky:
            return "POINT"

        # 3. CLICK: Index + Middle fingers up
        if index and middle and not ring and not pinky:
            return "CLICK"

        # 4. DOUBLE_CLICK: Index + Middle + Ring fingers up
        if index and middle and ring and not pinky:
            return "DOUBLE_CLICK"

        # 5. RIGHT_CLICK: Index + Pinky OR Pinky only
        if (index and pinky and not middle and not ring) or (pinky and not index and not middle and not ring):
            return "RIGHT_CLICK"

        # 6. PALM_SCROLL: Open Palm (All 4 main fingers up) -> Move Palm UP/DOWN to scroll
        if index and middle and ring and pinky:
            return "PALM_SCROLL"

        return "NONE"

    def detect_gesture(self, fingers, pinch_distance=999):
        """
        Detect gesture and pass through temporal majority voting buffer to eliminate flicker.
        """
        raw_gesture = self._raw_detect(fingers, pinch_distance)
        self.history.append(raw_gesture)

        # Majority vote across consecutive frames
        most_common, count = Counter(self.history).most_common(1)[0]
        if count >= 2:
            self.last_stable_gesture = most_common

        return self.last_stable_gesture