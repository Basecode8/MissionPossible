import EventHandling
import HardwareDevices
import Events
import RPi.GPIO as GPIO
import threading

# Init all GPIO pins
IR_LedPin = 0;
IR_RecieverPin = 0;

redLedPin = 0;
lightDetectorPin = 0;

waterPin = 0;

thermometerPin = 0;

incandescentPin = 0;
solarPin = 0;

matchPin = 0;
pressurePin = 0;


# Initiate all devices
servo = HardwareDevices.Servo();  # Servo pin can be found in /boot/config
beam = HardwareDevices.Beam(IR_LedPin, IR_RecieverPin);
lightDetector = HardwareDevices.LightDetect(redLedPin, lightDetectorPin);
water = HardwareDevices.Water(waterPin);
thermometer = HardwareDevices.Thermometer(thermometerPin);
incandescentBulb = HardwareDevices.IncandescentBulb(incandescentPin);
solarPanel = HardwareDevices.SolarPanel(solarPin)
match = HardwareDevices.Match(matchPin);
pressureSensor = HardwareDevices.PressureSensor(pressurePin);
eventDispatcher = EventHandling.EventDispatcher();

beamConnectionHandler = EventHandling.BeamConnectionHandler()
lightDetectionHandler = EventHandling.LightDetectorHandler()

servo.enable()  # Start servo (just for good measure)

beam.turn_on_led()


