import cv2

def draw_ui(img, mode):

    # Top black bar
    cv2.rectangle(img, (0, 0), (450, 100), (0, 0, 0), -1)

    # Title
    cv2.putText(img, "AI PRESENTATION MODE", (10, 35),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

    # Mode indicator
    cv2.putText(img, f"MODE: {mode}", (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Border glow effect
    h, w, _ = img.shape
    cv2.rectangle(img, (5, 5), (w-5, h-5), (0, 255, 255), 2)

    return imgpython main.py