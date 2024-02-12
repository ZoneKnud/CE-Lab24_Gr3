# -*- coding: utf-8 -*-

import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)

# ISL29125 address, 0x44(68)
# Select configuation-1register, 0x01(01)
# 0x0D(13) Operation: RGB, Range: 360 lux, Res: 16 Bits
bus.write_byte_data(0x44, 0x01, 0x05)

time.sleep(1)

print("Reading colour values and displaying them in a new window\n")

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def getAndUpdateColour():
	while True:
	# Read the data from the sensor
		# Insert code here
		# read_byte(i2c_addr,force=None) – To read a single byte from a device.
		# read_byte_data(i2c_addr,register,force=None) – To read a single byte from a designated register.
		# read_block_data(i2c_addr,register,force=None) – To read a block of up to 32-bytes from a given register.
		# read_i2c_block_data(i2c_addr,register,length,force=None) – To read a block of byte data from a given register.
		readdata = bus.read_i2c_block_data(0x44, 0x09, 6)
		print(readdata)

		red = readdata[3] << 8 | readdata[2]
		green = readdata[1] << 8 | readdata[0]
		blue = readdata[5] << 8 | readdata[4]

		blue = blue * 2

		# red = int(readdata[3])*256 + int(readdata[2])
		# green = int(readdata[1])*256 + int(readdata[0])
		# blue = int(readdata[5])*256 + int(readdata[4])

		print("red:   " + str(red))
		print("green: " + str(green))
		print("blue:  " + str(blue))


		if isclose(red, green, abs_tol = 800) and isclose(green, blue, abs_tol = 800) and isclose(red, blue, abs_tol = 800) and green <= 3000:
			print("BLACK!!!")
		elif isclose(red, green, abs_tol = 5000) and isclose(green, blue, abs_tol = 5000) and isclose(red, blue, abs_tol = 5000) and green > 10000:
			print("WHITE!!!")
		# elif isclose(green, blue, abs_tol = 5000) and green > red and blue > red:
		# 	print("CYAN!!!")
		# elif isclose(red, blue, abs_tol = 5000) and red > green and blue > green:
		# 	print("PURPLE!!")
		# elif isclose(red, green, abs_tol = 5000) and red > blue and green > blue:
		# 	print("YELLOW!!!")
		elif red > green and red > blue:
			print("RED!!!")
		elif green > red and green > blue:
			print("GREEN!!!")
		else:
			print("BLUE!!!")

		# BLÅ farve:
		# red:   4499
		# green: 9995
		# blue:  6333

		



		# Convert the data to green, red and blue int values
		# Insert code here
		
		
		# Output data to the console RGB values
		# Uncomment the line below when you have read the red, green and blue values
		# print("RGB(%d %d %d)" % (red, green, blue))
		print()
		
		time.sleep(2) 

getAndUpdateColour()