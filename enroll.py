import os
import cv2

from config import DB_DIR, CAM_INDEX
from utils import ensure_dir, load_face_detector, detect_largest_face, crop_and_resize

def enroll_person(name: str, samples: int = 30):
    ensure_dir(DB_DIR)
    person_dir = os.path.join(DB_DIR, name)
    ensure_dir(person_dir)

    det = load_face_detector()
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        raise RuntimeError("Webcam not accessible.")

    print(f"[ENROLL] {name} | target={samples}")
    print("SPACE = save sample | ESC = quit")

    saved = 0
    while saved < samples:
        ok, frame = cap.read()
        if not ok:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        box = detect_largest_face(det, gray)

        if box is not None:
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name} {saved}/{samples}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            cv2.putText(frame, "No face detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Enroll", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC
            break
        if key == 32 and box is not None:  # SPACE
            face = crop_and_resize(gray, box)
            out = os.path.join(person_dir, f"{name}_{saved:03d}.png")
            cv2.imwrite(out, face)
            saved += 1

    cap.release()
    cv2.destroyAllWindows()
    print(f"[ENROLL] saved {saved} samples -> {person_dir}")

if __name__ == "__main__":
    name = input("Citizen name: ").strip()
    samples = int(input("Samples (30 recommended): ").strip() or "30")
    enroll_person(name, samples=samples)
