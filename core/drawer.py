import cv2

LABELS = {
    "next":    ">> Next Slide",
    "prev":    "<< Prev Slide",
    "pointer": "Pointer Mode",
    "palm":"Close presentation"
}

def draw_ui(frame, gesture):
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w, 55), (0, 0, 0), -1)
    cv2.putText(frame, "LEFT=Next  |  RIGHT=Prev  |  1Finger=Pointer | OpenPalm=Close" ,
                (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)

    label = LABELS.get(gesture, "")
    if label:
        cv2.putText(frame, label, (w//2 - 150, h//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4)
    return frame