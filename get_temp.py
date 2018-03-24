#!/usr/bin/python

import smbus
import time
import argparse

#0 = /dev/i2c-0
#1 = /dev/i2c-1
I2C_BUS=1
bus = smbus.SMBus( I2C_BUS )

interval = 10
DEVICE_ADDRESS = 0x48
count = 0
total = 0

def post_temp( temp ):
    print "TEMP = %3.1f F" % ( temp_fahr )

def main( options ):
    sample = 0
    temps = []

    sleep_time = float( options.interval ) / options.samples
    print "Sleep_time:", sleep_time

    while True:
        temp_reg_12bit = bus.read_word_data( DEVICE_ADDRESS, 0 )
        temp_low = (temp_reg_12bit & 0xff00 ) >> 8
        temp_high = (temp_reg_12bit & 0x00ff )

        temp = ((( temp_high * 256 ) + temp_low ) >> 4 )

        if temp > 0x7ff:
            temp = temp - 4096

        temp_celsius = float( temp ) * 0.0625
        temp_fahr = temp_celsius * 9/5 + 32

        temps += [temp_fahr]
        print "Temp:", temp_fahr

        sample = (sample + 1) % options.samples 
        if sample == 0:
            total = sum( temps )
            avg = float( total ) / options.samples
            print temps
            print "\tMax:", max( temps )
            print "\tMin:", min( temps )
            print "\tAvg:", avg

            total = 0
            temps = []

        time.sleep( sleep_time )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( '-i', dest='interval', default=20, type=int )
    parser.add_argument( '-s', dest='samples', default=20, type=int )
    args = parser.parse_args()
    main( args )
