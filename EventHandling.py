import threading
import time

import Events


class Event:
    def __init__(self, event_type, data=None):
        self._type = event_type
        self._data = data

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data


class EventDispatcher(object):
    def __init__(self):
        self._events = dict()

    def __del__(self):
        self._events = None

    def has_listener(self, event_type, listener):
        if event_type in self._events.keys():
            return listener in self._events[event_type]
        else:
            return False

    def dispatch_event(self, event):
        if event.type in self._events.keys():
            listeners = self._events[event.type]

            for listener in listeners:
                listener[0](listener[1])  # The first item in the array is the function, and the second is the arguments

    def add_event_listener(self, event_type, listener, *args):
        if not self.has_listener(event_type, listener):
            listeners = self._events.get(event_type, [])

            listeners.append([listener, *args])

            self._events[event_type] = listeners

    def remove_event_listener(self, event_type, listener):
        if self.has_listener(event_type, listener):
            listeners = self._events[event_type]

            if len(listeners) == 1:
                del self._events[event_type]

            else:
                listeners.remove(listener)

                self._events[event_type] = listeners


class BeamHandler(object):
    def __init__(self, beam, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.beam = beam
        self.is_done = True
        self.thread = threading.Thread()
        self.connected()

    def _connected(self):
        while self.thread.is_alive():
            while True:
                if self.beam.pulsesPerHalfSecond() > 0:
                    self.event_dispatcher.dispatch_event(
                        Events.MPEvent(Events.MPEvent.BEAM_CONNECTED, self)
                    )

                else:
                    self.event_dispatcher.dispatch_event(
                        Events.MPEvent(Events.MPEvent.BEAM_DISCONNECTED, self)
                    )

                    break

                time.sleep(0.5)

    def connected(self):
        threading.Thread(target=self._connected, name=self.beam).run()


class ServoHandler(object):
    def __init__(self, servo, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.servo = servo

        self.event_dispatcher.add_event_listener(Events.MPEvent.RED_LED_NOT_DETECTED, self.servo.update, *(0,))
        self.event_dispatcher.add_event_listener(Events.MPEvent.RED_LED_DETECTED, self.servo.update, *(90,))


class LightDetectorHandler(object):
    def __init__(self, light_detector, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.light_detector = light_detector
        self.event_dispatcher.add_event_listener(Events.MPEvent.BEAM_DISCONNECTED, self.detected)
        self.thread = threading.Thread()
        self.detected()

    def _detected(self):
        while self.thread.is_alive():
            led_detected = False
            while not led_detected:
                if self.light_detector.read:
                    self.event_dispatcher.dispatch_event(
                        Events.MPEvent(Events.MPEvent.RED_LED_DETECTED, self)
                    )

                    led_detected = True

                else:
                    self.event_dispatcher.dispatch_event(
                        Events.MPEvent(Events.MPEvent.RED_LED_NOT_DETECTED, self)
                    )

                time.sleep(0.5)

    def detected(self):
        threading.Thread(target=self._detected, name=self.light_detector).run()


class WaterHandler(object):
    def __init__(self, event_dispatcher, water):
        self.event_dispatcher = event_dispatcher
        self.water = water
        self.thread = threading.Thread()
        self.detect()

    def _detect(self):
        while self.thread.is_alive():
            water_detected = False
            while not water_detected:
                if self.water.read():
                    self.event_dispatcher.dispatch_event(
                        Events.MPEvent(Events.MPEvent.WATER_DETECTED, self)
                    )
                    water_detected = True

    def detect(self):
        threading.Thread(target=self._detect, name=self.water).run()


class ThermometerHandler(object):
    def __init__(self, thermometer, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.thermometer = thermometer
        self.thread = threading.Thread()
        self.detect()

    def _detect(self):
        while self.thread.is_alive():
            initial_temp = self.thermometer.read_temp()[1]  # Gets temperature in Fahrenheit
            while self.thermometer.read_temp()[1] > initial_temp - 2:
                time.sleep(0.1)

            self.event_dispatcher.dispatch_event(
                Events.MPEvent(Events.MPEvent.TEMPERATURE_FALLEN, self)
            )

    def detect(self):
        threading.Thread(target=self._detect, name=self.thermometer).run()


class IncandescentHandler(object):
    def __init__(self, incandescent_bulb, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.incandescent_bulb = incandescent_bulb
        self.event_dispatcher.add_event_listener(Events.MPEvent.TEMPERATURE_FALLEN, self.therm_detected)

    def therm_detected(self):
        self.incandescent_bulb.turn_on()


class SolarHandler(object):
    def __init__(self, solar_panel, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.solar_panel = solar_panel
        self.thread = threading.Thread()
        self.detect()

    def _detect(self):
        while self.thread.is_alive():
            light_detected = False
            while not light_detected:
                if self.solar_panel.read():
                    self.event_dispatcher.dispatch_event(
                        Events.MPEvent(Events.MPEvent.SOLAR_PANEL_DETECTED, self)
                    )

                    light_detected = True

    def detect(self):
        threading.Thread(target=self._detect, name=self.solar_panel).run()


class MatchHandler(object):
    def __init__(self, match, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.match = match
        self.event_dispatcher.add_event_listener(Events.MPEvent.SOLAR_PANEL_DETECTED, self.solar_panel_detected)

    def solar_panel_detected(self):
        self.match.turn_on()
        time.sleep(1)

        self.match.turn_off()


class PressureHandler(object):
    def __init__(self, pressure_sensor, event_dispatcher):
        self.pressure_sensor = pressure_sensor
        self.event_dispatcher = event_dispatcher
        self.thread = threading.Thread()
        self.detect()

    def _detect(self):
        while self.thread.is_alive():
            pressure_detected = False
            while not pressure_detected:
                if self.pressure_sensor.read():
                    self.event_dispatcher.dispatch_event(
                        Events.MPEvent(Events.MPEvent.PRESSURE_DETECTED, self)
                    )
                    pressure_detected = True

    def detect(self):
        self.thread = threading.Thread(target=self._detect, name=self.pressure_sensor).run()