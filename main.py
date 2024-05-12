from readFromLightSensor import lightSensorRead
# from readFromSonar import sonarSensorRead
from leds import gpioLED


import time
import RPi.GPIO as GPIO
import json
import requests


lightSensor = lightSensorRead()
# sonarSensor = sonarSensorRead()

# ledRed = gpioLED(26)
# ledGreen = gpioLED(16)

recent_colors = []

led = gpioLED(16)
led.turnOn()


red_count = 0
green_count = 0
blue_count = 0

start_time = time.time()


try:

	while True:
		# ledRed.turnOn()
		# ledRedtimestamp = time.time()
		# distance = sonarSensor.measure()
		# print("  Distance : %.1f cm" % distance)
		# timing = distance**2 / 1000
		
		# if distance <= 20:
		# 	if ledRed.timestamp + timing <= time.time():
		# 		if ledRed.state == "off":
		# 			ledRed.turnOn()
		# 			ledGreen.turnOff()
		# 		else:
		# 			ledRed.turnOff()
				
		# 		ledRed.timestamp = time.time()
		# else:
		# 	if ledGreen.timestamp + timing <= time.time():
		# 		if ledGreen.state == "off":
		# 			ledGreen.turnOn()
		# 			ledRed.turnOff()
		# 		else:
		# 			ledGreen.turnOff()
				
		# 		ledGreen.timestamp = time.time()
  
		# time.sleep(0.5)

		
		lightSensor.getAndUpdateColour()
		print(lightSensor.currentColor)

		if start_time + 2 < time.time():
			
			recent_colors.append(lightSensor.currentColor)

			tmp_greycount = 0
			tmp_rgbcount = 0
			for i in range(len(recent_colors)):
				if recent_colors[i] == "red" or recent_colors[i] == "blue" or recent_colors[i] == "green":
					tmp_rgbcount += 1
				elif recent_colors[i] == "grey":
					tmp_greycount += 1
			
			print(recent_colors[-10:])		
			print(tmp_rgbcount)
			print(tmp_greycount)

			tmp_red = 0
			tmp_green = 0
			tmp_blue = 0


			if len(recent_colors) > 4 and tmp_greycount >= 3 and tmp_rgbcount >= 2 and all(i == "grey" for i in recent_colors[-3:]):
				most_recent_colors = list(recent_colors[-20:])
				for i in range(len(most_recent_colors)):
					if most_recent_colors[i] == "red":
						tmp_red += 1
					if most_recent_colors[i] == "green":
						tmp_green += 1
					if most_recent_colors[i] == "blue":
						tmp_blue += 1
				
				if tmp_red > tmp_blue and tmp_red > tmp_green:
					red_count += 1
				elif tmp_blue > tmp_red and tmp_blue > tmp_green:
					blue_count += 1
				else:
					green_count += 1

				print("tmp_red:   " + str(tmp_red))
				print("tmp_green: " + str(tmp_green))
				print("tmp_blue:  " + str(tmp_blue))
				
				recent_colors = []

			print("red_count:   " + str(red_count))
			print("green_count: " + str(green_count))
			print("blue_count:  " + str(blue_count))

			data_to_send = [lightSensor.currentColor] + [red_count, green_count, blue_count] + [lightSensor.red, lightSensor.green, lightSensor.blue]

			r = requests.post('http://192.168.137.1:5000/receive_data', json={"color": json.dumps(data_to_send)})

except KeyboardInterrupt:
	print("Stop")
	print(red_count)
	print(green_count)
	print(blue_count)
	GPIO.cleanup()