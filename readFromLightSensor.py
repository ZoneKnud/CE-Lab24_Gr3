# -*- coding: utf-8 -*-

import smbus
import time

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
	return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class lightSensorRead(object):

	def __init__(self):
		self.currentColor = "none"
		# For RGB sensor
		# Get I2C bus
		self.bus = smbus.SMBus(1)

		# ISL29125 address, 0x44(68)
		# Select configuation-1register, 0x01(01)
		# 0x0D(13) Operation: RGB, Range: 360 lux, Res: 16 Bits
		self.bus.write_byte_data(0x44, 0x01, 0x05)

	def getAndUpdateColour(self):
		# Read the data from the sensor
		# Insert code here
		# read_byte(i2c_addr,force=None) – To read a single byte from a device.
		# read_byte_data(i2c_addr,register,force=None) – To read a single byte from a designated register.
		# read_block_data(i2c_addr,register,force=None) – To read a block of up to 32-bytes from a given register.
		# read_i2c_block_data(i2c_addr,register,length,force=None) – To read a block of byte data from a given register.
		readdata = self.bus.read_i2c_block_data(0x44, 0x09, 6)
		# print(readdata)

		# Combine high byte and low byte by shifting high byte 8 bits to the left and OR with low bit.
		red = readdata[3] << 8 | readdata[2]
		green = readdata[1] << 8 | readdata[0]
		blue = readdata[5] << 8 | readdata[4]

		blue = blue * 2

		# red = int(readdata[3])*256 + int(readdata[2])
		# green = int(readdata[1])*256 + int(readdata[0])
		# blue = int(readdata[5])*256 + int(readdata[4])

		# print("red:   " + str(red))
		# print("green: " + str(green))
		# print("blue:  " + str(blue))


		if isclose(red, green, abs_tol = 800) and isclose(green, blue, abs_tol = 800) and isclose(red, blue, abs_tol = 800) and green <= 3000:
			# print("BLACK!!!")
			self.currentColor = "black"
		elif isclose(red, green, abs_tol = 5000) and isclose(green, blue, abs_tol = 5000) and isclose(red, blue, abs_tol = 5000) and green > 10000:
			# print("WHITE!!!")
			self.currentColor = "white"
		# elif isclose(green, blue, abs_tol = 5000) and green > red and blue > red:
		# 	print("CYAN!!!")
		# elif isclose(red, blue, abs_tol = 5000) and red > green and blue > green:
		# 	print("PURPLE!!")
		# elif isclose(red, green, abs_tol = 5000) and red > blue and green > blue:
		# 	print("YELLOW!!!")
		elif red > green and red > blue:
			# print("RED!!!")
			self.currentColor = "red"
		elif green > red and green > blue:
			# print("GREEN!!!")
			self.currentColor = "green"
		else:
			# print("BLUE!!!")
			self.currentColor = "blue"

