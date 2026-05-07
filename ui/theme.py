import cv2   # ← yeh line sabse upar add karo

class Colors:
    PRIMARY = (0, 255, 0)      # Green
    SECONDARY = (255, 0, 0)    # Blue
    WARNING = (0, 0, 255)      # Red
    BACKGROUND = (0, 0, 0)     # Black
    TEXT = (255, 255, 255)     # White

class Fonts:
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    SMALL = 0.5
    MEDIUM = 0.7
    LARGE = 1.0