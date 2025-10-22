# --- Ultrasonic ---
TRIG_BOTTLE, ECHO_BOTTLE = 17, 27
TRIG_BIN, ECHO_BIN = 22, 23

# --- Servo & Buzzer ---
SERVO_PIN = 18
BUZZER_PIN = 12

# --- LCD & Keypad ---
LCD_ADDR = 0x27
KEYPAD_ADDR = 0x20
I2C_BUS = 1

# --- Cameras ---
USER_CAMERA_INDEX = 0
BOTTLE_CAMERA_INDEX = 2

# --- File paths ---
USER_DATA_FILE = "data/users.json"
FACES_DIR = "data/faces/"

# --- Distance thresholds ---
BIN_FULL_DISTANCE = 8   # cm
BOTTLE_PRESENT_DISTANCE = 6
