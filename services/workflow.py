import time
import RPi.GPIO as GPIO
from Components.pins import Pins
from Components.ultrasonic import setup as us_setup, is_object_near
from Components.servo import Servo
from Components.buzzer import Buzzer
from Components.lcd_i2c import LCD
from Components.keypad_i2c import KeypadI2C
from services.auth import verify_or_register
from services.classify import classify_bottle
from services.points import allocate_points
from services.db import log_event

def run_cycle():
    GPIO.setmode(GPIO.BCM)
    # Setup hardware
    us_setup(Pins.ULTRASONIC1_TRIG, Pins.ULTRASONIC1_ECHO)
    us_setup(Pins.ULTRASONIC2_TRIG, Pins.ULTRASONIC2_ECHO)

    servo_lid = Servo(Pins.SERVO_LID)
    servo_route = Servo(Pins.SERVO_ROUTE)
    buzzer = Buzzer(Pins.BUZZER)
    lcd = LCD()
    keypad = KeypadI2C()

    GPIO.setup(Pins.BUTTON_START, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    try:
        lcd.write("ecoRewards", 0)
        lcd.write("Press start", 1)
        # Wait for button
        while GPIO.input(Pins.BUTTON_START) == 0:
            time.sleep(0.05)

        buzzer.beep(1)
        user_id = verify_or_register(lcd=lcd, keypad=keypad)
        log_event("user_verified", f"user_id={user_id}")

        # Open lid
        lcd.write("Opening lid...", 0)
        servo_lid.angle(90)

        # Wait for bottle
        lcd.write("Insert bottle", 1)
        t_start = time.time()
        while not is_object_near(Pins.ULTRASONIC1_TRIG, Pins.ULTRASONIC1_ECHO, threshold_cm=8):
            if time.time() - t_start > 15:
                lcd.write("Timeout", 0)
                servo_lid.angle(0)
                buzzer.beep(2)
                log_event("timeout", "no bottle inserted")
                return

        buzzer.beep(1)
        lcd.write("Detecting...", 0)

        # Trigger classification
        bottle_type, points = classify_bottle(camera_index=1)
        lcd.write(f"{bottle_type}: {points}pts", 1)
        log_event("classified", f"type={bottle_type}, points={points}")

        # Close lid
        time.sleep(1.0)
        servo_lid.angle(0)

        # Ask insert again (simple: press start within 5s)
        lcd.write("Press start to add", 0)
        lcd.write("or wait to finish", 1)
        t_again = time.time()
        while time.time() - t_again < 5:
            if GPIO.input(Pins.BUTTON_START) == 1:
                # Repeat cycle quickly: open lid and re-detect
                servo_lid.angle(90)
                while not is_object_near(Pins.ULTRASONIC1_TRIG, Pins.ULTRASONIC1_ECHO, threshold_cm=8):
                    time.sleep(0.05)
                bottle_type2, points2 = classify_bottle(camera_index=1)
                lcd.write(f"{bottle_type2}: {points2}pts", 1)
                log_event("classified", f"type={bottle_type2}, points={points2}")
                points += points2
                servo_lid.angle(0)
                t_again = time.time()  # extend window

        # Allocate points
        allocate_points(user_id, bottle_type, points)
        buzzer.beep(2, duration=0.08)
        lcd.write(f"Total +{points}", 0)
        lcd.write("Saved to DB", 1)
        log_event("points_allocated", f"user={user_id}, points={points}")

    finally:
        servo_lid.close()
        servo_route.close()
        GPIO.cleanup()