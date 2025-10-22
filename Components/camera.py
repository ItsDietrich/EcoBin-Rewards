import cv2

def capture_frame(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError("Camera capture failed")
    return frame

def save_image(frame, path):
    cv2.imwrite(path, frame)