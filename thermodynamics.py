import HardwareDevices
import time

thermometer = HardwareDevices.Thermometer()
temps = []

for i in range(0, 5):
    temps.append([thermometer.read_temp()])
    time.sleep(120)

print(temps)