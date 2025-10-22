from RPLCD.i2c import CharLCD
from time import sleep
from config_test import I2C_BUS, LCD_ADDR

lcd = CharLCD(i2c_expander='PCF8574', address=LCD_ADDR, port=I2C_BUS)

lcd.clear()
lcd.write_string("EcoBinRewards")
sleep(2)
lcd.clear()
lcd.write_string("LCD Test: OK!")
sleep(3)
lcd.clear()
lcd.write_string("Ready for Keypad")

print("LCD test completed successfully!")

