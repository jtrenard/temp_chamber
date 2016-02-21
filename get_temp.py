#!/usr/bin/python

import smbus

#0 = /dev/i2c-0
#1 = /dev/i2c-1
I2C_BUS=1
bus = smbus.SMBus( I2C_BUS )

DEVICE_ADDRESS = 0x48

temp_reg_12bit = bus.read_word_data( DEVICE_ADDRESS, 0 )
temp_low = (temp_reg_12bit & 0xff00 ) >> 8
temp_high = (temp_reg_12bit & 0x00ff )

temp = ((( temp_high * 256 ) + temp_low ) >> 4 )

if temp > 0x7ff:
	temp = temp - 4096

temp_C = float( temp ) * 0.0625
temp_F = temp_C * 9/5 + 32

print "TEMP = %3.1f C -- %3.1f F" % (temp_C, temp_F )
