import cv2
import numpy as np
import pyautogui
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.6, maxHands=1)
pyautogui.FAILSAFE = False

SCREEN_W, SCREEN_H = 1366, 768

def get_hands(frame):
    hands, frame = detector.findHands(frame, draw=True)
    return hands, frame

def run_system():
    from core.gesture import get_gesture, load_model
    from core.drawer import draw_ui
    from core.ppt_control import control_ppt

    load_model()
    
    from core.voice import start_voice
    start_voice()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not open!")
        return

    print("ON. Press Q to quit")
    print("LEFT=Next | RIGHT=Prev | 1Finger=Pointer | Palm=Pointer OFF")

    prev_gesture   = None
    pointer_active = False

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        h, w  = frame.shape[:2]
        hands, frame = get_hands(frame)
        gesture      = get_gesture(hands)
        frame        = draw_ui(frame, gesture)

        # ── POINTER MODE ──────────────────────────
        if pointer_active and hands:
            lmList = hands[0]["lmList"]
            cx, cy = lmList[8][0], lmList[8][1]
            # Dot camera pe
            cv2.circle(frame, (cx, cy), 15, (0, 165, 255), -1)
            cv2.circle(frame, (cx, cy), 20, (255, 255, 255), 2)
            # Mouse screen pe
            sx = int(np.interp(cx, [0, w], [0, SCREEN_W]))
            sy = int(np.interp(cy, [0, h], [0, SCREEN_H]))
            pyautogui.moveTo(sx, sy)

        # ── GESTURE ACTIONS ───────────────────────
        if gesture and gesture != prev_gesture:

            if gesture == "pointer":
                pointer_active = True
                print("☝️ Pointer ON")

            elif gesture == "palm":
                pointer_active = False
                print("✋ Pointer OFF")

            elif gesture in ("next", "prev"):
                # Sirf tab kaam kare jab pointer OFF ho
                if not pointer_active:
                    control_ppt(gesture)

            prev_gesture = gesture

        elif not gesture:
            prev_gesture = None

        # Status screen pe
        status = "POINTER MODE" if pointer_active else "NORMAL MODE"
        color  = (0, 165, 255) if pointer_active else (0, 255, 0)
        cv2.putText(frame, status, (10, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow("AI PPT Assistant", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()