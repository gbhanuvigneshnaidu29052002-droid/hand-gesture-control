class GestureController:
    """
    Maps finger states to specific gestures
    """

    def __init__(self):
        self.last_gesture = "NONE"

    def detect_gesture(self, fingers):
        """
        Detect gesture based on which fingers are up
        """

        # Only index finger up → cursor movement
        if fingers[1] and not fingers[2]:
            return "POINT"

        # Index + middle → single click
        elif fingers[1] and fingers[2] and not fingers[3]:
            return "CLICK"

        # Index + middle + ring → double click
        elif fingers[1] and fingers[2] and fingers[3]:
            return "DOUBLE_CLICK"

        return "NONE"