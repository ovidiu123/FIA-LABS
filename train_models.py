import os
import pandas as pd
from joblib import dump

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

DATASET = "boss_dataset.csv"
MODEL_DIR = "models"
BEST_MODEL_PATH = os.path.join(MODEL_DIR, "best_model.joblib")
BEST_INFO_PATH = os.path.join(MODEL_DIR, "best_model_info.txt")

LABELS = ["ANGRY", "NEUTRAL", "FORGIVING"]  # 0,1,2

def make_vectorizer():
    # multilingual friendly
    return TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5),
        lowercase=True
    )

def main():
    if not os.path.exists(DATASET):
        raise FileNotFoundError(f"Missing {DATASET}. Run make_dataset.py first.")

    df = pd.read_csv(DATASET)
    X = df["text"].astype(str).tolist()
    y = df["label"].astype(int).to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    models = {
        "LogisticRegression": LogisticRegression(max_iter=3000, multi_class="auto"),
        "LinearSVC": LinearSVC(),
        "MultinomialNB": MultinomialNB(),
    }

    best_name, best_score, best_pipeline = None, -1.0, None

    for name, clf in models.items():
        pipe = Pipeline([
            ("tfidf", make_vectorizer()),
            ("clf", clf),
        ])

        print(f"\n=== {name} ===")
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)

        acc = accuracy_score(y_test, pred)
        f1m = f1_score(y_test, pred, average="macro")  # important for 3 classes

        print("Accuracy:", round(acc, 4))
        print("Macro F1:", round(f1m, 4))
        print(classification_report(y_test, pred, target_names=LABELS, digits=4))
        print("Confusion matrix:\n", confusion_matrix(y_test, pred))

        if f1m > best_score:
            best_score = f1m
            best_name = name
            best_pipeline = pipe

    os.makedirs(MODEL_DIR, exist_ok=True)
    dump(best_pipeline, BEST_MODEL_PATH)

    with open(BEST_INFO_PATH, "w", encoding="utf-8") as f:
        f.write(f"Best model: {best_name}\nBest Macro F1: {best_score:.4f}\n")

    print(f"\n🏆 Best model: {best_name} | Macro F1={best_score:.4f}")
    print("Saved:", BEST_MODEL_PATH)

if __name__ == "__main__":
    main()
