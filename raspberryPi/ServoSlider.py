import RPi.GPIO as GPIO
from tkinter import *
import numpy as np
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 50)
p.start(0)

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        scale = Scale(frame, from_=0, to=180, length=300, width=30,
                      orient=HORIZONTAL, command=self.update)
        scale.grid(row=0)
        
    def update(self, angle):
        duty = (float(angle) / 180) * 9.05 + 2.4
        p.ChangeDutyCycle(duty)
        print(duty)


def on_closing():
    GPIO.cleanup()
    root.destroy()
    
root = Tk()
root.wm_title("Servo Control")
app = App(root)
root.geometry("600x150+0+0")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
