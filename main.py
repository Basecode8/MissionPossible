import EventHandling
import HardwareDevices
import threading
import time


# Init all GPIO pins
IR_LedPin = 0
IR_ReceiverPin = 0

redLedPin = 0
lightDetectorPin = 0

waterPin = 0

thermometerPin = 0

incandescentPin = 0
solarPin = 0

matchPin = 0


# Initiate all devices
beam = HardwareDevices.Beam(IR_LedPin, IR_ReceiverPin)
servo = HardwareDevices.Servo()  # Servo pin can be found in /boot/config
light_detector = HardwareDevices.LightDetect(redLedPin, lightDetectorPin)
water = HardwareDevices.Water(waterPin)
thermometer = HardwareDevices.Thermometer()
incandescent_bulb = HardwareDevices.IncandescentBulb(incandescentPin)
solar_panel = HardwareDevices.SolarPanel(solarPin)
match = HardwareDevices.Match(matchPin)
pressure_sensor = HardwareDevices.PressureSensor()  # Pressure sensor must be put on certain ports

event_dispatcher = EventHandling.EventDispatcher()  # Custom class to send events between threads

#  Here we initialize all of the device handlers
handlers = {
    "beam_connection_handler": EventHandling.BeamHandler(beam, event_dispatcher),
    "servo_handler": EventHandling.ServoHandler(servo, event_dispatcher),
    "light_detection_handler": EventHandling.LightDetectorHandler(light_detector, event_dispatcher),
    "water_handler": EventHandling.WaterHandler(water, event_dispatcher),
    "thermometer_handler": EventHandling.ThermometerHandler(thermometer, event_dispatcher),
    "incandescent_handler": EventHandling.IncandescentHandler(incandescent_bulb, event_dispatcher),
    "solar_handler": EventHandling.SolarHandler(solar_panel, event_dispatcher),
    "match_handler": EventHandling.MatchHandler(match, event_dispatcher),
    "pressure_handler": EventHandling.PressureHandler(pressure_sensor, event_dispatcher)
}


servo.enable()  # Start servo (just for good measure)

beam.turn_on_led()


try:
    while True:
        if len(handlers) == threading.active_count():
            print("Everything seems to be working")
        else:
            "Uh oh"
        time.sleep(5)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Finishing Up")
