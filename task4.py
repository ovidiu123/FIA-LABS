import pandas as pd

import os
print("Current working directory:", os.getcwd())
print("Files here:", os.listdir())

import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv("wine-quality-white-and-red.csv")



print("Dataset shape:", df.shape)
print(df.head())

# ----------------------------
# PREPROCESSING
# ----------------------------

# Convert quality into classes
def quality_class(q):
    if q <= 5:
        return "low"
    elif q <= 7:
        return "medium"
    else:
        return "high"

df["quality_label"] = df["quality"].apply(quality_class)

print("\nClass distribution:")
print(df["quality_label"].value_counts())

# Encode target labels
le = LabelEncoder()
y = le.fit_transform(df["quality_label"])

# Features
X = df.drop(["quality", "quality_label"], axis=1)

# If 'type' column exists, encode it
if "type" in X.columns:
    X["type"] = LabelEncoder().fit_transform(X["type"])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# ----------------------------
# MODELS
# ----------------------------
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "SVM (RBF)": SVC(kernel="rbf", gamma="auto")
}

results = {}

for name, model in models.items():
    print(f"\n=== {name} ===")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    print("Accuracy:", acc)
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    results[name] = confusion_matrix(y_test, y_pred)

# ----------------------------
# CONFUSION MATRICES
# ----------------------------
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for ax, (name, cm) in zip(axes, results.items()):
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_title(name)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

plt.tight_layout()
plt.show()
