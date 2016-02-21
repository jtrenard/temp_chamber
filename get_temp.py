#!/usr/bin/python

import smbus
import time

#0 = /dev/i2c-0
#1 = /dev/i2c-1
I2C_BUS=1
bus = smbus.SMBus( I2C_BUS )

interval = 10
DEVICE_ADDRESS = 0x48
count = 0
total = 0

while True:
    temp_reg_12bit = bus.read_word_data( DEVICE_ADDRESS, 0 )
    temp_low = (temp_reg_12bit & 0xff00 ) >> 8
    temp_high = (temp_reg_12bit & 0x00ff )

    temp = ((( temp_high * 256 ) + temp_low ) >> 4 )

    if temp > 0x7ff:
        temp = temp - 4096

    temp_celsius = float( temp ) * 0.0625
    temp_fahr = temp_celsius * 9/5 + 32

    total += temp_fahr
    count+=1
    if( count % interval ):
        print "TEMP = %3.1f F" % ( temp_fahr )
    time.sleep(1.0)
