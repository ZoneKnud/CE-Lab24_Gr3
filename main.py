from readFromLightSensor import lightSensorRead
from readFromSonar import sonarSensorRead
from leds import gpioLED


import time
import RPi.GPIO as GPIO


lightSensor = lightSensorRead()
sonarSensor = sonarSensorRead()

ledRed = gpioLED(26)
ledGreen = gpioLED(16)


try:

	while True:
		# ledRed.turnOn()
		# ledRedtimestamp = time.time()
		distance = sonarSensor.measure()
		print("  Distance : %.1f cm" % distance)
		timing = distance**2 / 1000
		
		if distance <= 20:
			if ledRed.timestamp + timing <= time.time():
				if ledRed.state == "off":
					ledRed.turnOn()
					ledGreen.turnOff()
				else:
					ledRed.turnOff()
				
				ledRed.timestamp = time.time()
		else:
			if ledGreen.timestamp + timing <= time.time():
				if ledGreen.state == "off":
					ledGreen.turnOn()
					ledRed.turnOff()
				else:
					ledGreen.turnOff()
				
				ledGreen.timestamp = time.time()

		
		lightSensor.getAndUpdateColour()
		print(lightSensor.currentColor)
		print("")

except KeyboardInterrupt:
	print("Stop")
	GPIO.cleanup()