import os
import cv2
from typing import Optional, Tuple

from config import FACE_SIZE

Box = Tuple[int, int, int, int]

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def load_face_detector():
    cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    det = cv2.CascadeClassifier(cascade_path)
    if det.empty():
        raise RuntimeError("Failed to load Haar cascade.")
    return det

def detect_largest_face(detector, gray) -> Optional[Box]:
    faces = detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(70, 70)
    )
    if len(faces) == 0:
        return None
    return sorted(faces, key=lambda b: b[2] * b[3], reverse=True)[0]

def crop_and_resize(gray, box: Box):
    x, y, w, h = box
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, FACE_SIZE, interpolation=cv2.INTER_AREA)
    return face
