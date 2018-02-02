import RPi.GPIO as GPIO
import EventHandling
import time
from pwm import PWM
from gpiozero import LightSensor
import Adafruit_BMP.BMP085 as BMP085


class Servo(object):
    def __init__(self, channel=0):
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
        # Gets pulse time in ms to change period of PWM
        duty = round((float(angle) / 180 * 1.8 + 0.7) * 1000000)
        self._pwm.duty_cycle = duty


class Beam(object):
    def __init__(self, led_pin_num, receiver_pin_num, channel=1):
        self.led_pin_num = led_pin_num
        self.reciever_pin_num = receiver_pin_num
        GPIO.setup(led_pin_num, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(receiver_pin_num, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Setup PWM for led
        self._pwm = PWM(channel)  # The servo is defaulted to 0 and this is defaulted to 1, so be careful
        self._pwm.export()
        self._pwm.period = 32258064  # About 31 pulses per second (seems to be max of receiver)
        self._pwm.duty_cycle = 0  # Will start with LED off
        self._pwm.enable = True

    def turn_on_led(self):
        self._pwm.duty_cycle = 32258064

    def turn_off_led(self):
        self._pwm.duty_cycle = 0

    def pulsesPerHalfSecond(self):
        pulses = [0]

        def pulse(ev=None):  # The event_detect gives this param and throws errors if it not defined
            pulses[0] += 1

        GPIO.add_event_detect(self.receiver_pin_num, GPIO.FALLING, pulse)
        time.sleep(0.5)
        GPIO.remove_event_detect(self.reciever_pin_num)
        return pulses[0]

class LightDetect(LightSensor):
    def __init__(self, ledPin, photoresistorPin):
        self.ledPin = ledPin
        self.photoresistorPin = photoresistorPin

        self.lightSensor = super(photoresistorPin)  # photoresistorPin is initialized here
        GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.LOW)

    def read(self):
        return self.lightSensor.light_detected()

    def turn_on_led(self):
        GPIO.output(self.ledPin, GPIO.HIGH)

    def turn_off_led(self):
        GPIO.output(self.ledPin, GPIO.LOW)


class Water(object):
    def __init__(self, waterPin):
        self.waterPin = waterPin
        self.event = event
        self.eventDispatcher = eventDispatcher

        GPIO.setup(waterPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read(self):
        return GPIO.input(self.waterPin)


# Thermometer class here


class IncandescentBulb(object):
    def __init__(self, incandescentPin):
        self.incandescentPin = incandescentPin
        GPIO.setup(incandescentPin, GPIO.OUT, initial=GPIO.LOW)

    def turn_on(self):
        GPIO.output(self.incandescentPin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.incandescentPin, GPIO.LOW)


class SolarPanel(object):
    def __init__(self, solarPin, event, eventDispatcher):
        self.solarPin = solarPin
        self.event = event
        self.eventDispatcher = eventDispatcher

        GPIO.setup(solarPin, GPIO.OUT, initial=GPIO.LOW)

    def read(self):
        return GPIO.input(self.solarPin)


class Match(object):
    def __init__(self, matchPin):
        self.matchPin = matchPin
        GPIO.setup(matchPin, GPIO.OUT, initial=GPIO.LOW)

    def turn_on(self):
        GPIO.output(self.matchPin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.matchPin, GPIO.LOW)


class PressureSensor(object):
    def __init__(self):
        self.event = eventDispatcher
        self.eventDispatcher = eventDispatcher
        self.sensor = BMP085.BMP085()

    def read(self):
        return self.sensor.read_pressure()