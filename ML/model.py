import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os


df = pd.read_csv("data/hand_gestures.csv")
print(df.head())

X = df.iloc[:, :63].values
y = df['label'].values

print(X.shape)
print(pd.Series(y).value_counts())
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    min_samples_split=2,
    random_state=42)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(accuracy*100)


os.makedirs("models", exist_ok=True)
model_path = "models/gesture_model.pkl"

joblib.dump(model, model_path)

labels = np.unique(y)
joblib.dump(labels, "models/random_forest.pkl")
