import RPi.GPIO as GPIO
import time

class gpioLED(object):
	def __init__(self, ledPIN):
		self.ledPIN = ledPIN
		self.state = "off"
		self.timestamp = 0
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.ledPIN,GPIO.OUT)

	def turnOn(self):
		print("LED on")
		GPIO.output(self.ledPIN,GPIO.HIGH)
		self.state = "on"
	
	def turnOff(self):
		print("LED off")
		GPIO.output(self.ledPIN,GPIO.LOW)
		self.state = "off"
