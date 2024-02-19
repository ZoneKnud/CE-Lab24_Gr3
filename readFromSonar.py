import time
import RPi.GPIO as GPIO


class sonarSensorRead(object):

		def __init__(self):
			# Use BCM GPIO references
			# instead of physical pin numbers
			GPIO.setmode(GPIO.BCM)

			# Define GPIO to use on Pi
			self.GPIO_TRIGECHO = 18

			print("Ultrasonic Measurement")

			# Set pins as output and input
			GPIO.setup(self.GPIO_TRIGECHO,GPIO.OUT)  # Initial state as output


			# Set trigger to False (Low)
			GPIO.output(self.GPIO_TRIGECHO, False)

		def measure(self):
			# This function measures a distance
			# Pulse the trigger/echo line to initiate a measurement
			GPIO.output(self.GPIO_TRIGECHO, True)
			time.sleep(0.00001)
			GPIO.output(self.GPIO_TRIGECHO, False)
			#ensure start time is set in case of very quick return
			start = time.time()

			# set line to input to check for start of echo response
			GPIO.setup(self.GPIO_TRIGECHO, GPIO.IN)
			while GPIO.input(self.GPIO_TRIGECHO)==0:
					start = time.time()

			# Wait for end of echo response
			while GPIO.input(self.GPIO_TRIGECHO)==1:
					stop = time.time()
		
			GPIO.setup(self.GPIO_TRIGECHO, GPIO.OUT)
			GPIO.output(self.GPIO_TRIGECHO, False)

			elapsed = stop-start
			distance = (elapsed * 34300)/2.0
			# As the sound advances 340m per second (equal 34300 cm). 
			# The distance can be obtained by multiplying the speed and the elapsed time. 
			# That is, the distance is 34300 * elpsed time(ms)
			# Divide by two because of the sound travels forwards and backwards.

			# time.sleep(0.1)
			return distance






