import os
import pandas as pd

OUT_CSV = "boss_dataset.csv"

def main():
    # label: 0=ANGRY, 1=NEUTRAL, 2=FORGIVING

    angry = [
        "You're late again. Unacceptable.",
        "This is not what I asked for. Fix it now.",
        "Stop making excuses. Deliver results.",
        "This is sloppy work. Redo it.",
        "You ignored the instructions.",
        "Not good enough. Improve it.",
        "Correct it immediately.",
        "I am disappointed. Do it properly.",
        "Iar ai întârziat. Inacceptabil.",
        "Nu e ce am cerut. Repară imediat.",
        "Nu mă interesează scuzele. Vreau rezultate.",
        "E făcut de mântuială. Refă.",
        "Ты снова опоздал. Неприемлемо.",
        "Это не то, что я просил. Исправь сейчас.",
        "Хватит оправданий. Нужен результат.",
        "Сделано плохо. Переделай.",
    ]

    neutral = [
        "hello",
        "hi",
        "ok",
        "okay",
        "k",
        "thanks",
        "thank you",
        "noted",
        "received",
        "understood",
        "please update me",
        "send me the status",
        "let me know when it's ready",
        "bună",
        "salut",
        "ok",
        "bine",
        "am înțeles",
        "primit",
        "спасибо",
        "понял",
        "ок",
        "принято",
    ]

    forgiving = [
        "Good job. Thanks for handling it.",
        "This is better. Keep going.",
        "I appreciate the effort.",
        "Alright, we can move forward.",
        "You fixed it. Well done.",
        "Nice improvement compared to last time.",
        "Ok, that works. Thanks.",
        "Good progress. Continue.",
        "Bine lucrat. Mulțumesc.",
        "E mai bine. Continuă așa.",
        "Apreciez efortul.",
        "Ok, mergem mai departe.",
        "Ai rezolvat. Bravo.",
        "Хорошая работа. Спасибо.",
        "Стало лучше. Продолжай.",
        "Идём дальше. Хорошо.",
    ]

    rows = [(t, 0) for t in angry] + [(t, 1) for t in neutral] + [(t, 2) for t in forgiving]
    df = pd.DataFrame(rows, columns=["text", "label"])
    df.to_csv(OUT_CSV, index=False, encoding="utf-8")

    print("✅ Dataset created offline")
    print("Path:", os.path.abspath(OUT_CSV))
    print("Rows:", len(df))
    print(df.sample(8, random_state=1))

if __name__ == "__main__":
    main()
