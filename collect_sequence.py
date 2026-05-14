import cv2
import numpy as np
import os
import time
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)

SEQUENCE_LENGTH = 20  # 20 frames ki sequence
GESTURES = {
    "next": "Hand — fast swipe",
    "prev": "Hand — fast swipe",
    "none": "Hand — still"
}
SAMPLES_PER_GESTURE = 200

os.makedirs("data/sequences", exist_ok=True)

def normalize(lmList):
    wrist_x = lmList[0][0]
    wrist_y = lmList[0][1]
    coords = []
    for lm in lmList:
        coords.append(lm[0] - wrist_x)
        coords.append(lm[1] - wrist_y)
    max_val = max(abs(v) for v in coords) or 1
    return [v / max_val for v in coords]

all_sequences = []
all_labels = []

for gesture, instruction in GESTURES.items():
    print(f"\n{'='*55}")
    print(f"  Gesture: {gesture.upper()}")
    print(f"  Karo: {instruction}")
    print(f"  5 second mein shuru...")
    print(f"{'='*55}")

    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    print("  *** RECORDING ***\n")

    cap = cv2.VideoCapture(0)
    count = 0
    sequence_buffer = []

    while count < SAMPLES_PER_GESTURE:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        hands, frame = detector.findHands(frame, draw=True)

        # Progress
        progress = int((count / SAMPLES_PER_GESTURE) * 500)
        cv2.rectangle(frame, (10, 10), (510, 45), (30,30,30), -1)
        cv2.rectangle(frame, (10, 10), (10+progress, 45), (0,200,0), -1)
        cv2.putText(frame, f"{gesture.upper()}: {count}/{SAMPLES_PER_GESTURE}",
                    (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(frame, instruction,
                    (15, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 1)
        cv2.imshow("Sequence Collection", frame)

        if hands:
            lmList = hands[0]["lmList"]
            if len(lmList) == 21:
                features = normalize(lmList)
                sequence_buffer.append(features)

                # 20 frames ki sequence complete hoi
                if len(sequence_buffer) == SEQUENCE_LENGTH:
                    all_sequences.append(sequence_buffer.copy())
                    all_labels.append(gesture)
                    sequence_buffer = []
                    count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"  ✅ {gesture}: {count} sequences done!")

# Save
np.save("data/sequences/X.npy", np.array(all_sequences))
np.save("data/sequences/y.npy", np.array(all_labels))

print(f"\n✅ Total sequences: {len(all_sequences)}")
print(f"Shape: {np.array(all_sequences).shape}")
print("Now run train_lstm.py !")
