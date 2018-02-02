import EventHandling


class MPEvent(EventHandling.Event):
    BEAM_CONNECTED = "connectedMyEvent"
    BEAM_DISCONNECTED = "disconnectedMyEvent"
    RED_LED_DETECTED = "redLedDetected"
    RED_LED_NOT_DETECTED = "redLedNotDetected"
    WATER_DETECTED = "waterDetected"
    TEMPERATURE_FALLEN = "temperatureFallen"
    SOLAR_PANEL_DETECTED = "solarPanelDetected"
    PRESSURE_DETECTED = "pressureDetected"
