import os
import glob
import RPi.GPIO as GPIO
from tkinter import *
import numpy as np
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 50)
p.start(0)

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def update_servo(angle):
    duty = (float(angle) / 180) * 9.05 + 2.4
    p.ChangeDutyCycle(duty)

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

baseTemp = read_temp()[1];
try:
    while True:
        currentTemp = read_temp()[1]
        if currentTemp >= baseTemp + 0.5:
            update_servo(90)
            print("success!")
            print(baseTemp, currentTemp)
        else:
            update_servo(0)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting")
