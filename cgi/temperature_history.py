#!/usr/bin/python3

# Turn on debug mode.
import os
import cgitb
import sqlite3
import datetime
cgitb.enable()

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def generate_png( cursor, start, end, filename ):
    query = '''SELECT * FROM "temps" WHERE read_datetime BETWEEN "%s" AND 
    "%s"''' % ( start, end )

    cursor.execute( query )

    temp_list = []
    print( '<p>' )
    all = cursor.fetchall()
    for thing in all:
        #print(thing, '<br>')
        temp_list += thing[1].strip('[]').split(',')

    float_temps = [float(temp) for temp in temp_list]

    print( '</p>' )

    plt.plot(float_temps)
    plt.savefig('graphs/%s' % (filename))


# Print necessary headers.
print("Content-Type: text/html" )
print('')

print("temperature history")

today=datetime.datetime.now()
today_str = today.strftime("%Y-%m-%dT%H:%M:%S")
print("today: ", today_str )
lasttwentyfour = today - datetime.timedelta( seconds = 24*60*60 )
lasttwentyfour_str = lasttwentyfour.strftime("%Y-%m-%dT%H:%M:%S")
print("lasttwentyfour: ", lasttwentyfour_str )

try:
    db = sqlite3.connect('./env_stats.db' )
except:
    print( 'failed to connect to database' )

try:
    cursor = db.cursor()
except:
    print( 'db.cursor() failed' )

generate_png( cursor, lasttwentyfour_str, today_str, '24hours.png' )

twoweeks = today - datetime.timedelta( days=14)
twoweeks_str = twoweeks.strftime("%Y-%m-%dT%H:%M:%S")
print( "<br>twoweeks_str: ", twoweeks_str )
generate_png( cursor, twoweeks_str, today_str, '2weeks.png' )

print( '<h2>Last 24 Hours</h2>' )
print( '<img src="graphs/24hours.png">' )

print( '<h2>Last 2 Weeks</h2>' )
print( '<img src="graphs/2weeks.png">' )

print( '<h2>Last 24 Hours</h2>' )
print( '<img src="graphs/lastyear.png">' )

db.close()
