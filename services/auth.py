import os
import cv2
import face_recognition
from Components.camera import capture_frame, save_image
from services.db import get_user, upsert_user

USERS_DIR = "data/users"

def verify_or_register(lcd=None, keypad=None):
    if lcd: lcd.write("Press start", 0)
    # Capture face for verification
    frame = capture_frame(camera_index=0)
    os.makedirs(USERS_DIR, exist_ok=True)
    temp_path = "data/current_face.jpg"
    save_image(frame, temp_path)

    current_img = face_recognition.load_image_file(temp_path)
    encs = face_recognition.face_encodings(current_img)
    current_enc = encs[0] if encs else None

    # Walk users and compare
    matched_id = None
    if current_enc:
        for user_id in os.listdir(USERS_DIR):
            face_path = os.path.join(USERS_DIR, user_id, "face.jpg")
            if not os.path.exists(face_path): continue
            known_img = face_recognition.load_image_file(face_path)
            known_encs = face_recognition.face_encodings(known_img)
            if not known_encs: continue
            match = face_recognition.compare_faces([known_encs[0]], current_enc, tolerance=0.5)
            if match[0]:
                matched_id = user_id
                break

    if matched_id:
        if lcd: lcd.write(f"Hello, {matched_id}", 0)
        return matched_id

    # Register new user
    if lcd: lcd.write("Not registered", 0); lcd.write("Enter ID:", 1)
    user_id = keypad.read_id_blocking(lcd=lcd, prompt="Enter ID:")
    user_dir = os.path.join(USERS_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)
    reg_face_path = os.path.join(user_dir, "face.jpg")
    save_image(frame, reg_face_path)
    upsert_user(user_id, name=user_id, face_path=reg_face_path)
    if lcd: lcd.write("Registered!", 0)
    return user_id