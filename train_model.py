import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import pickle

print("Data load ho raha hai...")
df = pd.read_csv("data/gestures.csv")
print(f"Total: {len(df)} | Gestures: {df['label'].unique()}")

X = df.drop("label", axis=1).values
y = df["label"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Model train ho raha hai — 1-2 minute...")

model = GradientBoostingClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)

acc = accuracy_score(y_test, model.predict(X_test))
print(f"\n{'='*40}")
print(f"✅ Accuracy: {acc*100:.1f}%")
print(f"{'='*40}")
print(classification_report(y_test, model.predict(X_test)))

with open("models/gesture_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model saved!")
print("Ab main.py chalao!")