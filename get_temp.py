#!/usr/bin/python

import smbus
import time
import datetime
import argparse
import sqlite3

#0 = /dev/i2c-0
#1 = /dev/i2c-1
I2C_BUS=1
bus = smbus.SMBus( I2C_BUS )

DEVICE_ADDRESS = 0x48

sqlite_db_file = './env_stats.db'

def post_temps( temps ):

    now = datetime.datetime.now()
    #str_now = now.strftime( '%B %d, %Y %I:%M%p' )
    str_now = now.strftime( '%Y-%m-%d %I:%M%p' )

    db = sqlite3.connect( sqlite_db_file )
    cursor = db.cursor()

    sql_query = '''INSERT INTO temps( read_datetime, readings ) 
    VALUES("%s","%s")'''% ( str_now, str( temps ) )
    print "query:", sql_query 

    try:
        cursor.execute( sql_query )
    except:
        db.close()
        return

    db.commit()
    db.close()

def get_temp():
    temp_reg_12bit = bus.read_word_data( DEVICE_ADDRESS, 0 )
    temp_low = (temp_reg_12bit & 0xff00 ) >> 8
    temp_high = (temp_reg_12bit & 0x00ff )

    temp = ((( temp_high * 256 ) + temp_low ) >> 4 )

    if temp > 0x7ff:
        temp = temp - 4096

    temp_celsius = float( temp ) * 0.0625
    temp_fahr = temp_celsius * 9/5 + 32
    return temp_fahr


def main( options ):
    sample = 0
    temps = []

    sleep_time = float( options.interval ) / options.samples
    if options.verbose:
        print "Sleep_time:", sleep_time

    while True:
        temp_fahr = get_temp()

        temps += [temp_fahr]
        if options.verbose:
            print "Temp:", temp_fahr

        sample = (sample + 1) % options.samples 
        if sample == 0:
            total = sum( temps )
            avg = float( total ) / options.samples
            post_temps( temps )
            if options.verbose:
                print temps
                print "\tMax:", max( temps )
                print "\tMin:", min( temps )
                print "\tAvg:", avg

            total = 0
            temps = []

        time.sleep( sleep_time )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( '-i', dest='interval', default=60, type=int )
    parser.add_argument( '-s', dest='samples', default=20, type=int )
    parser.add_argument( '-v', dest='verbose', action="store_true", 
                        default=False )
    args = parser.parse_args()
    main( args )
