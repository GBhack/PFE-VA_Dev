from Adafruit_I2C import Adafruit_I2C
import time

i2c = Adafruit_I2C(0x04,2)

while True:
    i2c.readU16(0)
    time.sleep(0.5)