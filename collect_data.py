import cv2
import csv
import os
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector

detector = HandDetector(detectionCon=0.8, maxHands=1)
os.makedirs("data", exist_ok=True)
os.makedirs("models", exist_ok=True)

def normalize(lmList):
    wrist_x = lmList[0][0]
    wrist_y = lmList[0][1]
    coords = []
    for lm in lmList:
        coords.append(lm[0] - wrist_x)
        coords.append(lm[1] - wrist_y)
    max_val = max(abs(v) for v in coords) or 1
    return [v / max_val for v in coords]

def collect(gesture, instruction, samples):
    print(f"\n{'='*55}")
    print(f"  Gesture: {gesture.upper()}")
    print(f"  Action: {instruction}")
    print(f"  Starting in 5 seconds...")
    print(f"{'='*55}")
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    print("  *** RECORDING ***\n")

    cap = cv2.VideoCapture(0)
    data = []
    count = 0

    while count < samples:
        success, frame = cap.read()
        if not success:
            break
        frame = cv2.flip(frame, 1)
        hands, frame = detector.findHands(frame, draw=True)

        progress = int((count / samples) * 500)
        cv2.rectangle(frame, (10, 10), (510, 45), (30,30,30), -1)
        cv2.rectangle(frame, (10, 10), (10+progress, 45), (0,200,0), -1)
        cv2.putText(frame, f"{gesture.upper()}: {count}/{samples}",
                    (15, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(frame, instruction,
                    (15, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 1)
        cv2.imshow("Collecting", frame)

        if hands:
            lmList = hands[0]["lmList"]
            if len(lmList) == 21:
                row = normalize(lmList)
                row.append(gesture)
                data.append(row)
                count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"  ✅ {count} samples done!")
    return data

all_data = []

# NEXT — only LEFT movement
print("\n⚠️  For NEXT: Move hand QUICKLY to the LEFT")
print("    Wrist should move LEFT in camera view")
all_data += collect("next",
    "Swipe hand LEFT — move your WRIST", 600)

# PREV — only RIGHT movement  
print("\n⚠️  For PREV: Move hand QUICKLY to the RIGHT")
print("    Wrist should move RIGHT in camera view")
all_data += collect("prev",
    "Swipe hand RIGHT — move your WRIST", 600)

# POINTER — ONLY index finger, others CLOSED
print("\n⚠️  POINTER: Raise ONLY index finger")
print("    ALL OTHER FINGERS MUST BE CLOSED")
all_data += collect("pointer",
    "ONLY index finger UP — others completely closed", 500)

# NONE — no movement
print("\n⚠️  NONE: Keep hand STILL — no movement")
all_data += collect("none",
    "Open palm — completely STILL — no movement", 500)

# Save
header = [f"{a}{i}" for i in range(21) for a in ["x","y"]]
header.append("label")

with open("data/gestures.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(all_data)

print(f"\n✅ Total: {len(all_data)} samples saved!")
print("Now run train_model.py!")