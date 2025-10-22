import time
import pigpio
from config_test import SERVO_PIN

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    exit("❌ Pigpio daemon not running. Run: sudo pigpiod")

# Helper function
def set_servo_angle(angle):
    """Set servo angle (0 to 180 degrees)."""
    pulse_width = 500 + (angle / 180) * 2000
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

try:
    print("🧠 Servo Test: Moving to 0°, 90°, 180° repeatedly...")
    while True:
        for angle in [0, 90, 180, 90]:
            set_servo_angle(angle)
            print(f" → Servo at {angle}°")
            time.sleep(1)

except KeyboardInterrupt:
    print("\nTest stopped by user.")
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    pi.stop()
