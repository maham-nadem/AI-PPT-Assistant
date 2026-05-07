import pickle
import numpy as np
import os
import time
from collections import deque

model = None
last_time = 0
COOLDOWN = 1.2
wrist_history = deque(maxlen=8)
pointer_counter = 0

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
    """Check karo ke haath fully open hai"""
    tip_ids = [8, 12, 16, 20]  # index, middle, ring, pinky tips
    base_ids = [6, 10, 14, 18]  # unke bases
    
    fingers_up = 0
    for tip, base in zip(tip_ids, base_ids):
        if lmList[tip][1] < lmList[base][1]:  # tip base se upar hai
            fingers_up += 1
    
    return fingers_up >= 4  # 4 ya zyada fingers up = palm

def get_gesture(hands):
    global last_time, pointer_counter

    if model is None or not hands:
        wrist_history.clear()
        pointer_counter = 0
        return None

    lmList = hands[0]["lmList"]
    if len(lmList) != 21:
        return None

    wrist_x = lmList[0][0]
    wrist_history.append(wrist_x)

    features = np.array(normalize(lmList)).reshape(1, -1)
    prediction = model.predict(features)[0]
    confidence = model.predict_proba(features).max()

    now = time.time()

    # ── PALM CHECK ────────────────────────────────
    if is_palm_open(lmList):
        positions = list(wrist_history)
        if len(positions) >= 4:
            swing = max(positions) - min(positions)
            if swing < 20:  # haath still hai
                pointer_counter = 0
                if now - last_time > COOLDOWN:
                    last_time = now
                    return "palm"
        return None

    # ── POINTER ───────────────────────────────────
    if prediction == "pointer" and confidence > 0.95:
        pointer_counter += 1
        if pointer_counter >= 15 and now - last_time > COOLDOWN:
            last_time = now
            pointer_counter = 0
            return "pointer"
        return None
    else:
        pointer_counter = 0

    if now - last_time < COOLDOWN:
        return None

    if len(wrist_history) < 6:
        return None

    # ── NEXT / PREV ───────────────────────────────
    positions = list(wrist_history)
    total_swing = max(positions) - min(positions)
    movement = positions[-1] - positions[0]

    if total_swing < 60:
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