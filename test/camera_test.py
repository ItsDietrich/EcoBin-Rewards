import cv2
from config_test import USER_CAMERA_INDEX, BOTTLE_CAMERA_INDEX

cam1 = cv2.VideoCapture(USER_CAMERA_INDEX)
cam2 = cv2.VideoCapture(BOTTLE_CAMERA_INDEX)

# Optional: set resolution
cam1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cam2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cam1.isOpened():
    print(f" Camera {USER_CAMERA_INDEX} not detected.")
else:
    print(f" Camera {USER_CAMERA_INDEX} detected and opened successfully.")

if not cam2.isOpened():
    print(f" Camera {BOTTLE_CAMERA_INDEX} not detected.")
else:
    print(f" Camera {BOTTLE_CAMERA_INDEX} detected and opened successfully.")

print("\nPress 'q' to exit the camera preview.")

while True:
    ret1, frame1 = cam1.read()
    ret2, frame2 = cam2.read()

    if not ret1:
        print(f" Could not read from camera {USER_CAMERA_INDEX}")
        break
    if not ret2:
        print(f" Could not read from camera {BOTTLE_CAMERA_INDEX}")
        break

    # Combine both frames horizontally for display
    combined = cv2.hconcat([frame1, frame2])

    cv2.imshow("EcoBinRewards - Camera 1 (Left) | Camera 2 (Right)", combined)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release cameras and close windows
cam1.release()
cam2.release()
cv2.destroyAllWindows()
