import os
import cv2
import numpy as np

from config import DB_DIR, MODEL_PATH, LABELS_PATH, CONF_THRESHOLD, FACE_SIZE
from utils import ensure_dir

def load_db():
    if not os.path.isdir(DB_DIR):
        raise RuntimeError(f"Missing DB folder: {DB_DIR}")

    X, y = [], []
    label_to_name = {}
    label = 0

    for person in sorted(os.listdir(DB_DIR)):
        pdir = os.path.join(DB_DIR, person)
        if not os.path.isdir(pdir):
            continue

        label_to_name[label] = person
        for fn in os.listdir(pdir):
            if fn.lower().endswith((".png", ".jpg", ".jpeg")):
                img = cv2.imread(os.path.join(pdir, fn), cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue
                img = cv2.resize(img, FACE_SIZE, interpolation=cv2.INTER_AREA)
                X.append(img)
                y.append(label)

        label += 1

    if len(X) < 20:
        raise RuntimeError("Not enough images. Enroll 2+ people with ~20-30 samples each.")
    return X, np.array(y, dtype=np.int32), label_to_name

def train_model(test_ratio: float = 0.25, seed: int = 42):
    if not hasattr(cv2, "face"):
        raise RuntimeError("cv2.face not found. Install opencv-contrib-python.")

    X, y, label_to_name = load_db()
    rng = np.random.default_rng(seed)
    idx = np.arange(len(X))
    rng.shuffle(idx)
    X = [X[i] for i in idx]
    y = y[idx]

    split = int(len(X) * (1 - test_ratio))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
    model.train(X_train, y_train)

    correct = 0
    for img, true_label in zip(X_test, y_test):
        pred, conf = model.predict(img)
        if conf <= CONF_THRESHOLD and pred == true_label:
            correct += 1
    acc = correct / max(1, len(X_test))

    model.save(MODEL_PATH)
    np.save(LABELS_PATH, label_to_name)

    print(f"[TRAIN] train={len(X_train)} test={len(X_test)}")
    print(f"[TRAIN] threshold={CONF_THRESHOLD} | test accuracy={acc:.3f}")
    print(f"[TRAIN] saved -> {MODEL_PATH}")
    print(f"[TRAIN] labels saved -> {LABELS_PATH}")

if __name__ == "__main__":
    ensure_dir(DB_DIR)
    train_model()
