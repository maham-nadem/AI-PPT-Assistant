import pickle
import numpy as np
import os
import time
from collections import deque

model = None
last_time = 0
COOLDOWN = 1.5
wrist_history = deque(maxlen=8)
pointer_counter = 0
palm_counter = 0

def normalize(lmList):
    wrist_x = lmList[0][0]
    wrist_y = lmList[0][1]
    coords = []
    for lm in lmList:
        coords.append(lm[0] - wrist_x)
        coords.append(lm[1] - wrist_y)
    max_val = max(abs(v) for v in coords) or 1
    return [v / max_val for v in coords]

def load_model():
    global model
    if os.path.exists("models/gesture_model.pkl"):
        with open("models/gesture_model.pkl", "rb") as f:
            model = pickle.load(f)
        print("✅ ML Model ready!")
    else:
        print("❌ Model nahi mila!")

def is_palm_open(lmList):
    tip_ids  = [8, 12, 16, 20]
    base_ids = [6, 10, 14, 18]
    fingers_up = sum(1 for t, b in zip(tip_ids, base_ids)
                     if lmList[t][1] < lmList[b][1])
    return fingers_up >= 4

def get_gesture(hands):
    global last_time, pointer_counter, palm_counter

    if model is None or not hands:
        wrist_history.clear()
        pointer_counter = 0
        palm_counter = 0
        return None

    lmList = hands[0]["lmList"]
    if len(lmList) != 21:
        return None

    wrist_x = lmList[0][0]
    wrist_history.append(wrist_x)

    now = time.time()

    # ── 1. PALM (4+ fingers up, haath still) ─────
    if is_palm_open(lmList):
        palm_counter += 1
        pointer_counter = 0
        if palm_counter == 20 and now - last_time > 2.0:
            last_time = now
            return "palm"
        return None
    else:
        palm_counter = 0

    # ── 2. POINTER (model prediction) ────────────
    features = np.array(normalize(lmList)).reshape(1, -1)
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features).max()

    if prediction == "pointer" and confidence > 0.90:
        pointer_counter += 1
        if pointer_counter >= 7 and now - last_time > COOLDOWN:
            last_time = now
            pointer_counter = 0
            return "pointer"
        return None
    else:
        pointer_counter = 0

    # ── 3. NEXT / PREV (movement) ─────────────────
    if now - last_time < COOLDOWN:
        return None
    if len(wrist_history) < 6:
        return None

    positions = list(wrist_history)
    swing     = max(positions) - min(positions)
    movement  = positions[-1] - positions[0]

    if swing < 60:
        return None

    if movement < -40:
        last_time = now
        wrist_history.clear()
        return "next"
    elif movement > 40:
        last_time = now
        wrist_history.clear()
        return "prev"

    return None