import RPi.GPIO as GPIO
import time
from config_test import BUZZER_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

try:
    print("🔊 Testing active buzzer... Beep sequence starting.")
    for i in range(3):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(0.2)
    print("✅ Buzzer test complete.")
except KeyboardInterrupt:
    print("\nTest stopped by user.")
finally:
    GPIO.cleanup()
