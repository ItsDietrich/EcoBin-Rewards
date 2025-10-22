from smbus2 import SMBus
import time

# Simple HD44780 via I2C backpack (PCF8574). Adjust address as discovered by i2cdetect.
LCD_ADDR = 0x27
BUS_NUM = 1

# Minimal 4-bit mode writer (abstracted for brevity):
class LCD:
    def __init__(self, addr=LCD_ADDR, bus_num=BUS_NUM):
        self.addr = addr
        self.bus = SMBus(bus_num)
        self._init()

    def _write(self, data):
        self.bus.write_byte(self.addr, data)

    def _strobe(self, data):
        self._write(data | 0x04)
        time.sleep(0.0005)
        self._write(data & ~0x04)
        time.sleep(0.0001)

    def _send(self, data, mode):
        high = mode | (data & 0xF0) | 0x08
        low  = mode | ((data << 4) & 0xF0) | 0x08
        self._strobe(high); self._strobe(low)

    def _init(self):
        time.sleep(0.05)
        self.cmd(0x33); self.cmd(0x32); self.cmd(0x28); self.cmd(0x0C); self.cmd(0x06); self.cmd(0x01)

    def cmd(self, cmd):
        self._send(cmd, 0x00)

    def write(self, text, line=0):
        addr = 0x80 + (0x40 * line)
        self.cmd(addr)
        for ch in text.ljust(16)[:16]:
            self._send(ord(ch), 0x01)