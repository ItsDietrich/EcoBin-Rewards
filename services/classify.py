import torch
import torchvision.transforms as T
import cv2
from Components.camera import capture_frame

# Simple mock points; replace with your trained model
POINTS_MAP = {"PET": 10, "Glass": 15, "Aluminum": 20}

class DummyClassifier:
    def __init__(self):
        pass
    def predict(self, img_bgr):
        # TODO: replace with actual model inference
        return "PET"

def classify_bottle(camera_index=1):
    frame = capture_frame(camera_index)
    clf = DummyClassifier()
    label = clf.predict(frame)
    points = POINTS_MAP.get(label, 5)
    return label, points