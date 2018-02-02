import RPi.GPIO as GPIO
import os
import time
from customListeners import *
from pwm import PWM

GPIO.setmode(GPIO.BCM)
os.system("clear")

class Servo(object):
    def __init__(self, channel = 0):
        self._pwm = PWM(channel)
        self._pwm.export()
        self._pwm.period = 50000000
        self._pwm.duty_cycle = 0
        self._pwm.enable = True
	
    def enable(self):
        self._pwm.enable = True

    def disable(self):
        self._pwm.enable = False

    def update(self, angle):
        #Gets pulse time in ms to change period of PWM
        duty = round((float(angle)/180 * 1.8 + 0.7) * 1000000)
        self._pwm.duty_cycle = duty

class Beam(object):
    def __init__(self, pinNum):
        GPIO.setup(pinNum, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self._pinNum = pinNum

    @property
    def pinNum(self):
        return self._pinNum

    def pulsesPerHalfSecond(self):
        pulses = [0]
        def pulse(ev=None):
            pulses[0] += 1
        GPIO.add_event_detect(self._pinNum, GPIO.FALLING, pulse)
        time.sleep(0.5)
        GPIO.remove_event_detect(self._pinNum)
        return pulses[0]

class MyEvent(Event):
    CONNECTED = "connectedMyEvent"
    DISCONNECTED = "disconnectedMyEvent"


class ConnectionStatus(object):
    def __init__(self, event_dispatcher, beam):
        self.event_dispatcher = event_dispatcher
        self._beam = beam
        self.isDone = True

    def connected(self):
        self.isDone = False
        if self._beam.pulsesPerHalfSecond() != 0:
            self.event_dispatcher.dispatch_event(
                MyEvent(MyEvent.CONNECTED, self)
            )
        else:
            self.event_dispatcher.dispatch_event(
                MyEvent(MyEvent.DISCONNECTED, self)
            )
        self.isDone = True


class UpdateServo(object):
    
    def __init__(self, event_dispatcher, servo):
        self.servo = servo
        self.event_dispatcher = event_dispatcher
        
        self.event_dispatcher.add_event_listener(
            MyEvent.CONNECTED, self.on_connection_event
        )

        self.event_dispatcher.add_event_listener(
            MyEvent.DISCONNECTED, self.on_connection_event
        )
        
    def on_connection_event(self, event):
        if event.type == MyEvent.CONNECTED:
            self.servo.update(0)
        elif event.type == MyEvent.DISCONNECTED:
            self.servo.update(90)

try:
    servo1 = Servo(0)
    beam1 = Beam(17)
    dispatcher = EventDispatcher()
    connectionStatus = ConnectionStatus(dispatcher, beam1)
    updateServo1 = UpdateServo(dispatcher, servo1)
    while True:
        connectionStatus.connected()
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
    servo1.disable()
