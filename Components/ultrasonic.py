import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def setup(trig, echo):
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
    GPIO.output(trig, False)
    time.sleep(0.05)

def read_distance_cm(trig, echo, timeout=0.03):
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    t0 = time.time()
    while GPIO.input(echo) == 0:
        if time.time() - t0 > timeout:
            return None
    pulse_start = time.time()

    while GPIO.input(echo) == 1:
        if time.time() - pulse_start > timeout:
            return None
    pulse_end = time.time()

    duration = pulse_end - pulse_start
    return round(duration * 17150, 2)

def is_object_near(trig, echo, threshold_cm=10):
    d = read_distance_cm(trig, echo)
    return d is not None and d < threshold_cm