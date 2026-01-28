import time
import cv2
import numpy as np

from config import MODEL_PATH, LABELS_PATH, CONF_THRESHOLD, CAM_INDEX
from utils import load_face_detector, detect_largest_face, crop_and_resize

def run_realtime():
    if not hasattr(cv2, "face"):
        raise RuntimeError("cv2.face not found. Install opencv-contrib-python.")

    label_to_name = np.load(LABELS_PATH, allow_pickle=True).item()
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read(MODEL_PATH)

    det = load_face_detector()
    cap = cv2.VideoCapture(CAM_INDEX)
    if not cap.isOpened():
        raise RuntimeError("Webcam not accessible.")

    fps = 0.0
    last = time.time()

    print("[RUN] ESC to quit.")
    while True:
        ok, frame = cap.read()
        if not ok:
            continue

        t0 = time.time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        box = detect_largest_face(det, gray)

        if box is not None:
            x, y, w, h = box
            face = crop_and_resize(gray, box)
            pred, conf = model.predict(face)

            name = "Unknown"
            if conf <= CONF_THRESHOLD:
                name = label_to_name.get(pred, "Unknown")

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name} | conf={conf:.1f}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        now = time.time()
        dt = now - last
        if dt > 0:
            fps = 0.9 * fps + 0.1 * (1.0 / dt)
        last = now
        latency_ms = (time.time() - t0) * 1000.0

        cv2.putText(frame, f"FPS: {fps:.1f} | latency: {latency_ms:.1f} ms", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 0), 2)

        cv2.imshow("Luna-City Face Recognition (LBPH)", frame)
        if (cv2.waitKey(1) & 0xFF) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_realtime()
