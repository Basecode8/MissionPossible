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
                listener(event)

    def add_event_listener(self, event_type, listener):
        if not self.has_listener(event_type, listener):
            listeners = self._events.get(event_type, [])

            listeners.append(listener)

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
    def __init__(self, servo, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.servo = servo
        self.is_done = True

    def connected(self, beam):
        while True:
            if beam.pulsesPerHalfSecond() > 0:
                self.event_dispatcher.dispatch_event(
                    Events.MPEvent(Events.MPEvent.BEAM_CONNECTED, self)
                )

            else:
                self.event_dispatcher.dispatch_event(
                    Events.MPEvent(Events.MPEvent.BEAM_DISCONNECTED, self)
                )

                break

            time.sleep(0.5)


class LightDetectorHandler(object):
    def __init__(self, event_dispatcher, lightDetector):
        self.event_dispatcher = event_dispatcher
        self.lightDetector = lightDetector
        self.event_dispatcher.add_event_listener(Events.MPEvent.BEAM_DISCONNECTED, self.detected(self.lightDetector))

    def _detected(self, light_detector):
        led_detected = False
        while not led_detected:
            if light_detector.read:
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
        threading.Thread(target=self._detected(self.lightDetector))


class ServoHandler(object):
    def __init__(self, event_dispatcher, servo):
        self.event_dispatcher = event_dispatcher
        self.servo = servo

        self.event_dispatcher.add_event_listener(Events.MPEvent.RED_LED_NOT_DETECTED, self.servo.update(0))
        self.event_dispatcher.add_event_listener(Events.MPEvent.RED_LED_DETECTED, self.servo.update(90))


class WaterHandler(object):
    def __init__(self, event_dispatcher, water):
        self.event_dispatcher = event_dispatcher
        self.water = water

    def _detect(self):
        water_detected = False
        while not water_detected:
            if self.water.read():
                self.event_dispatcher.dispatch_event(
                    Events.MPEvent(Events.MPEvent.WATER_DETECTED, self)
                )
                water_detected = True

    def detect(self):
        threading.Thread(target=self._detect())


class ThermometerHandler(object):
    def __init__(self, thermometer, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.thermometer = thermometer

    def _detect(self):


    def detect(self):
        threading.Thread(target=self._detect())


class IncandescentHandler(object):
    def __init__(self, event_dispatcher, water):
        self.event_dispatcher = event_dispatcher
        self.water = water

    def _detect(self):
        water_detected = False
        while not water_detected:
            if self.water.read():
                self.event_dispatcher.dispatch_event(
                    Events.MPEvent(Events.MPEvent.WATER_DETECTED, self)
                )
                water_detected = True

    def detect(self):
        threading.Thread(target=self._detect())


class SolarHandler(object):
    def __init__(self, event_dispatcher, water):
        self.event_dispatcher = event_dispatcher
        self.water = water

    def _detect(self):
        water_detected = False
        while not water_detected:
            if self.water.read():
                self.event_dispatcher.dispatch_event(
                    Events.MPEvent(Events.MPEvent.WATER_DETECTED, self)
                )
                water_detected = True

    def detect(self):
        threading.Thread(target=self._detect())


class MatchHandler(object):
    def __init__(self, event_dispatcher, water):
        self.event_dispatcher = event_dispatcher
        self.water = water

    def _detect(self):
        water_detected = False
        while not water_detected:
            if self.water.read():
                self.event_dispatcher.dispatch_event(
                    Events.MPEvent(Events.MPEvent.WATER_DETECTED, self)
                )
                water_detected = True

    def detect(self):
        threading.Thread(target=self._detect())


class PressureHandler(object):
    def __init__(self, event_dispatcher, water):
        self.event_dispatcher = event_dispatcher
        self.water = water

    def _detect(self):
        water_detected = False
        while not water_detected:
            if self.water.read():
                self.event_dispatcher.dispatch_event(
                    Events.MPEvent(Events.MPEvent.WATER_DETECTED, self)
                )
                water_detected = True

    def detect(self):
        threading.Thread(target=self._detect())