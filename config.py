# Configuration file for camera and control parameters

# Camera resolution
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAM_WIDTH = CAMERA_WIDTH
CAM_HEIGHT = CAMERA_HEIGHT

# Hand Detector Performance Config (optimized for 30+ FPS)
MAX_HANDS = 1
MODEL_COMPLEXITY = 0
DETECTION_CONFIDENCE = 0.5
TRACKING_CONFIDENCE = 0.5

# Region reduction for stable boundary navigation
FRAME_REDUCTION = 80

# Smoothening factor for cursor movement (higher = smoother)
SMOOTHENING = 5

# Pinch threshold (pixels between thumb and index tips)
PINCH_THRESHOLD = 30

# Temporal majority voting buffer size (eliminates gesture flicker)
BUFFER_SIZE = 4

# Non-blocking gesture cooldown delays & scroll config
CLICK_DELAY = 0.45

# Gentle Palm Motion Scroll Config
SCROLL_SPEED = 40          # Base gentle scroll step
SCROLL_SENSITIVITY = 3.5    # Multiplier for palm vertical velocity
SCROLL_DEADZONE = 5        # Pixels of vertical palm movement required to trigger scroll
SCROLL_COOLDOWN = 0.04     # Smooth 25Hz scroll update rate