import time
import Adafruit_BBIO.GPIO as GPIO

header = 0
while header != 8 and header != 9:
    header= int(input(('Header number (8 or 9) ?')))

pin = 0
while pin != 999:
    pin = int(input('pin ?'))
    try:
        GPIO.setup("P"+str(header)+"_"+str(pin), GPIO.OUT)
        GPIO.output("P"+str(header)+"_"+str(pin), GPIO.HIGH)
        print('HIGH')
        time.sleep(2)
        GPIO.output("P"+str(header)+"_"+str(pin), GPIO.LOW)
        print('LOW')
    except:
        pass
