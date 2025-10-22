import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class Servo:
    def __init__(self, pin, freq=50):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)
        self.pwm = GPIO.PWM(pin, freq)
        self.pwm.start(0)

    def angle(self, deg):
        duty = 2 + (deg / 18.0)  # approx map 0..180 -> 2..12
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.4)
        self.pwm.ChangeDutyCycle(0)

    def close(self):
        self.pwm.stop()