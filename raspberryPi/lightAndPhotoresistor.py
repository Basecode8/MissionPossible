from gpiozero import LightSensor

lightSensor = LightSensor(27)

lightSensor.wait_for_dark()
print("Dark")
