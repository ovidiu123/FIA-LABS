import os
from joblib import load

MODEL_PATH = os.path.join("models", "best_model.joblib")

LABELS = {
    0: "ANGRY",
    1: "NEUTRAL",
    2: "FORGIVING",
}

# Greetings / short acknowledgements -> neutral
NEUTRAL_WORDS = {
    "hi", "hello", "hey", "yo",
    "ok", "okay", "k",
    "thanks", "thank you",
    "salut", "buna", "bună", "mersi",
    "okey",
    "привет", "здравствуй", "ок", "спасибо",
}

def force_neutral(msg: str) -> bool:
    s = msg.strip().lower()
    if not s:
        return True
    # very short messages are usually neutral
    if len(s) <= 3:
        return True
    # exact matches
    if s in NEUTRAL_WORDS:
        return True
    # common short patterns
    if s in {"good morning", "good evening", "bună ziua", "bună seara"}:
        return True
    return False

def main():
    print("Boss mood interpreter (OFFLINE, 3-class with neutral rule)")
    print("Rule: greetings / very short messages => NEUTRAL\n")

    if not os.path.exists(MODEL_PATH):
        print("⚠️ Model not found at:", MODEL_PATH)
        print("Run train_models.py first.\n")
        return

    model = load(MODEL_PATH)

    while True:
        msg = input("Boss> ")
        if msg.strip().lower() in ("exit", "quit", "q"):
            break

        if force_neutral(msg):
            print("Prediction:", LABELS[1], "(rule)\n")
            continue

        # If you trained only 2-class model, this will output 0/1.
        pred = int(model.predict([msg])[0])

        # Map 2-class models: 0=ANGRY, 1=FORGIVING
        if pred in (0, 1) and 2 not in LABELS:
            pass

        # If model is 2-class, treat label 1 as FORGIVING
        if pred == 1 and 2 in LABELS:
            # could be NEUTRAL or FORGIVING depending on training.
            # We'll assume 2-class training means 1=FORGIVING.
            print("Prediction:", LABELS[2], "(model)\n")
        elif pred == 0:
            print("Prediction:", LABELS[0], "(model)\n")
        elif pred == 1:
            print("Prediction:", LABELS[1], "(model)\n")
        else:
            print("Prediction:", LABELS.get(pred, f"UNKNOWN({pred})"), "(model)\n")

if __name__ == "__main__":
    main()
