import RPi.GPIO as GPIO
import os
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
connected = False
pulses = 0
os.system("clear")

def pulse(ev=None):
    global pulses
    pulses += 1
    
try:
    GPIO.add_event_detect(17, GPIO.FALLING, pulse, 2)
    while True:
        pulses = 0
        time.sleep(0.1)
        if pulses != 0 and not connected:
            connected = True
            os.system("clear")
            print("CONNECTED")
        elif pulses == 0 and connected:
            connected = False
            os.system("clear")
            print("BROKEN!")
        
except KeyboardInterrupt:
    GPIO.cleanup()
