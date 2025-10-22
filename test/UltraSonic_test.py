# test_ultrasonic.py
import RPi.GPIO as GPIO
import time
from config_test import TRIG_BOTTLE, ECHO_BOTTLE, TRIG_BIN, ECHO_BIN

GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG_BOTTLE, GPIO.OUT)
GPIO.setup(ECHO_BOTTLE, GPIO.IN)
GPIO.setup(TRIG_BIN, GPIO.OUT)
GPIO.setup(ECHO_BIN, GPIO.IN)

def measure_distance(TRIG, ECHO):
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ECHO) == 0:
        start_time = time.time()
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()

    # Time difference between send and receive
    elapsed = stop_time - start_time
    distance = (elapsed * 34300) / 2
    return distance

try:
    while True:
        dist1 = measure_distance(TRIG_BOTTLE, ECHO_BOTTLE)
        dist2 = measure_distance(TRIG_BIN, ECHO_BIN)
        print(f"Sensor 1: {dist1:.2f} cm | Sensor 2: {dist2:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nTest stopped by user.")
    GPIO.cleanup()

    GPIO.cleanup()
