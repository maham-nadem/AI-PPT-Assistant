import torch
import torch.nn as nn
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Data load
print("Data load ho raha hai...")
X = np.load("data/sequences/X.npy")
y = np.load("data/sequences/y.npy")

# Labels encode karo
le = LabelEncoder()
y_encoded = le.fit_transform(y)

print(f"Classes: {le.classes_}")
print(f"X shape: {X.shape}")

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# Tensors banao
X_train = torch.FloatTensor(X_train)
X_test  = torch.FloatTensor(X_test)
y_train = torch.LongTensor(y_train)
y_test  = torch.LongTensor(y_test)

# LSTM Model
class GestureLSTM(nn.Module):
    def __init__(self, input_size=42, hidden_size=128, num_layers=2, num_classes=3):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers,
                           batch_first=True, dropout=0.3)
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])
        return out

model = GestureLSTM(num_classes=len(le.classes_))
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Training
print("\nLSTM train ho raha hai...")
EPOCHS = 50

for epoch in range(EPOCHS):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        model.eval()
        with torch.no_grad():
            test_out = model(X_test)
            predicted = torch.argmax(test_out, dim=1)
            acc = (predicted == y_test).float().mean()
            print(f"Epoch {epoch+1}/{EPOCHS} | Loss: {loss:.4f} | Accuracy: {acc*100:.1f}%")

# Final accuracy
model.eval()
with torch.no_grad():
    test_out  = model(X_test)
    predicted = torch.argmax(test_out, dim=1)
    acc = (predicted == y_test).float().mean()

print(f"\n{'='*40}")
print(f"✅ Final Accuracy: {acc*100:.1f}%")
print(f"{'='*40}")

# Save
os.makedirs("models", exist_ok=True)
torch.save(model.state_dict(), "models/lstm_model.pth")
with open("models/lstm_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("✅ LSTM Model saved!")
print("Now main.py update !")