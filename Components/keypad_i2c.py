from smbus2 import SMBus
import time

# Example for TTP229 or similar I2C keypad; adjust address/reading per module datasheet
KEYPAD_ADDR = 0x20
BUS_NUM = 1

class KeypadI2C:
    def __init__(self, addr=KEYPAD_ADDR, bus_num=BUS_NUM):
        self.bus = SMBus(bus_num)
        self.addr = addr

    def read_key(self):
        # Read status register; map to character
        data = self.bus.read_byte(self.addr)
        # Map data to key; placeholder mapping:
        keymap = {0x01: '0', 0x02: '1', 0x04: '2', 0x08: '3', 0x10: '4', 0x20: '5', 0x40: '6', 0x80: '7'}
        return keymap.get(data, None)

    def read_id_blocking(self, lcd=None, prompt="Enter ID:"):
        buf = ""
        if lcd: lcd.write(prompt, 0)
        while True:
            k = self.read_key()
            if k is None:
                time.sleep(0.05); continue
            if k == '#':  # end
                return buf
            elif k == '*':  # backspace
                buf = buf[:-1]
            else:
                buf += k
            if lcd: lcd.write(f"ID: {buf}", 1)