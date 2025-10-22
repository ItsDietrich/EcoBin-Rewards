import smbus2
import time
from RPLCD.i2c import CharLCD
from config_test import I2C_BUS, KEYPAD_ADDR, LCD_ADDR

bus = smbus2.SMBus(I2C_BUS)

# ===========================
# LCD Setup
# ===========================
lcd = CharLCD(i2c_expander='PCF8574', address=LCD_ADDR, port=I2C_BUS)
lcd.clear()
lcd.write_string("EcoBinRewards")
time.sleep(2)
lcd.clear()
lcd.write_string("Enter User ID:")

# ===========================
# Keypad Configuration (4x4)
# ===========================
KEYPAD = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

ROWS = [0x01, 0x02, 0x04, 0x08]   # Bit masks for each row
COLS = [0x10, 0x20, 0x40, 0x80]   # Bit masks for each column

# ===========================
# Helper functions
# ===========================
def read_keypad():
    """
    Scans the keypad via PCF8574 and returns the pressed key, or None.
    """
    for row_index, row_mask in enumerate(ROWS):
        # Drive one row low (0) and others high (1)
        out_val = 0xF0 | (~row_mask & 0x0F)
        bus.write_byte(KEYPAD_ADDR, out_val)
        time.sleep(0.002)

        data = bus.read_byte(KEYPAD_ADDR)
        for col_index, col_mask in enumerate(COLS):
            if not (data & col_mask):
                return KEYPAD[row_index][col_index]
    return None


# ===========================
# Main Loop
# ===========================
user_input = ""

print("✅ LCD + I2C Keypad test running...")
print("Press digits to enter User ID.")
print("Press '*' to clear, '#' to confirm.")
try:
    last_input = ""  # Track previous input to avoid unnecessary clears
    lcd.clear()
    lcd.write_string("Enter User ID:\n")

    while True:
        key = read_keypad()
        if key:
            if key.isdigit():
                if len(user_input) < 10:
                    user_input += key
            elif key == "*":
                user_input = ""
            elif key == "#":
                lcd.clear()
                lcd.write_string(f"User ID:\n{user_input}")
                print(f"✅ User ID Entered: {user_input}")
                time.sleep(2)
                user_input = ""
                lcd.clear()
                lcd.write_string("Enter User ID:\n")

            # ✅ Only update the second line if input changed
            if user_input != last_input:
                lcd.cursor_pos = (1, 0)
                lcd.write_string(" " * 16)  # Clear line 2 only
                lcd.cursor_pos = (1, 0)
                lcd.write_string(user_input)
                last_input = user_input

            time.sleep(0.3)  # Debounce

except KeyboardInterrupt:
    lcd.clear()
    lcd.write_string("Exiting...")
    print("\n👋 Exiting gracefully...")
    time.sleep(1)
    lcd.clear()
