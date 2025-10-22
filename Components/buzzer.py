import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def beep(self, times=1, duration=0.1, gap=0.1):
        for _ in range(times):
            GPIO.output(self.pin, GPIO.HIGH)
            time.sleep(duration)
            GPIO.output(self.pin, GPIO.LOW)
            time.sleep(gap)