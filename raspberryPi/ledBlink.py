import RPi.GPIO as GPIO
import time

ledPin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

p = GPIO.PWM(ledPin, 31)
p.start(50)

try:
    while True:
        pass
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
    print("Done")
