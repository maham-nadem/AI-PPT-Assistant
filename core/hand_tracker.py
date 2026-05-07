import cv2
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.6, maxHands=1)

def get_hands(frame):
    hands, frame = detector.findHands(frame, draw=True)
    return hands, frame

def run_system():
    from core.gesture import get_gesture, load_model
    from core.drawer import draw_ui
    from core.ppt_control import control_ppt

    load_model()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not open!")
        return

    print("Start. Press Q to stop .")
    print("LEFT=Next | RIGHT=Prev | 1Finger=Pointer | Palm=Stop")

    prev_gesture = None

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        hands, frame = get_hands(frame)
        gesture = get_gesture(hands)
        frame = draw_ui(frame, gesture)

        if gesture == "pointer" and hands:
            lmList = hands[0]["lmList"]
            cx, cy = lmList[8][0], lmList[8][1]
            cv2.circle(frame, (cx, cy), 15, (0, 165, 255), -1)
            cv2.circle(frame, (cx, cy), 20, (255, 255, 255), 2)

        if gesture and gesture != prev_gesture:
            control_ppt(gesture)
            prev_gesture = gesture
        elif not gesture:
            prev_gesture = None

        cv2.imshow("AI PPT Assistant", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()