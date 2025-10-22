import RPi.GPIO as GPIO
import time
from config_test import BUZZER_PIN

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

buzzer = GPIO.PWM(BUZZER_PIN, 1000)  # Start with 1kHz

def beep(frequency, duration):
    buzzer.ChangeFrequency(frequency)
    buzzer.start(50)  # 50% duty cycle
    time.sleep(duration)
    buzzer.stop()
    time.sleep(0.05)

try:
    print(" Testing passive buzzer...")
    melody = [
        (1000, 0.2), (1500, 0.2), (2000, 0.2),
        (2500, 0.2), (3000, 0.2)
    ]
    for freq, dur in melody:
        beep(freq, dur)
    print("Buzzer test complete.")
except KeyboardInterrupt:
    buzzer.stop()
finally:
    GPIO.cleanup()
