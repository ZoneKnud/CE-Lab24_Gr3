# -*- coding: utf-8 -*-

import smbus
import time

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
	return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

class lightSensorRead(object):

	def __init__(self):
		self.currentColor = "none"
		self.red = 0
		self.blue = 0
		self.green = 0
		# For RGB sensor
		# Get I2C bus
		self.bus = smbus.SMBus(1)

		# ISL29125 address, 0x44(68)
		# Select configuation-1register, 0x01(01)
		# 0x0D(13) Operation: RGB, Range: 360 lux, Res: 16 Bits
		# write_byte_data(i2c_addr, register, value, force=None)
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
		self.red = readdata[3] << 8 | readdata[2]
		self.green = readdata[1] << 8 | readdata[0]
		self.blue = readdata[5] << 8 | readdata[4]

		print("red:   " + str(self.red))
		print("green: " + str(self.green))
		print("blue:  " + str(self.blue))


		if self.green > 50000 and self.red > 50000 and self.blue > 50000:
			self.currentColor = "white"
		
		elif self.red > 20000 and self.blue > 20000 and self.green > 20000:
			self.currentColor = "grey"

		elif self.red > self.green and self.red > self.blue + 7000:
			self.currentColor = "red"

		elif self.green > self.red + 10000 and self.green > self.blue + 5000:
			self.currentColor = "green"
			
		else:
			self.currentColor = "blue"
