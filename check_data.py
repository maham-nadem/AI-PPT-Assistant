import cv2
import numpy as np
import pickle
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)

with open("models/gesture_model.pkl", "rb") as f:
    model = pickle.load(f)

def normalize(lmList):
    wrist_x = lmList[0][0]
    wrist_y = lmList[0][1]
    coords = []
    for lm in lmList:
        coords.append(lm[0] - wrist_x)
        coords.append(lm[1] - wrist_y)
    max_val = max(abs(v) for v in coords) or 1
    return [v / max_val for v in coords]

cap = cv2.VideoCapture(0)
print("Test chal raha hai — haath dikhao, Q dabao band karne ke liye")

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame, draw=True)

    if hands:
        lmList = hands[0]["lmList"]
        if len(lmList) == 21:
            features = np.array(normalize(lmList)).reshape(1, -1)
            prediction = model.predict(features)[0]
            confidence = model.predict_proba(features).max()

            color = (0,255,0) if confidence > 0.90 else (0,0,255)
            cv2.putText(frame, f"{prediction} ({confidence*100:.0f}%)",
                        (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)

            # Confidence bar
            bar = int(confidence * 400)
            cv2.rectangle(frame, (10, 80), (410, 110), (50,50,50), -1)
            cv2.rectangle(frame, (10, 80), (10+bar, 110), color, -1)

            print(f"{prediction} — {confidence*100:.0f}%")

    cv2.imshow("Model Test", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()