import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from Adafruit_I2C import Adafruit_I2C

PWM.start("P9_16", 0)

GPIO.setup("P9_23", GPIO.OUT)

ATCON = Adafruit_I2C(0x04, 2)
ATCON.readU16(0)

ADC.setup()

print(ADC.read("AIN4"))
