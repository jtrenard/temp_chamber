#!/usr/bin/python3

# Turn on debug mode.
import os
import cgitb
import sqlite3
cgitb.enable()

# Print necessary headers.
print("Content-Type: text/html" )
print('')

print("temperature history")

try:
    db = sqlite3.connect('./env_stats.db' )
except:
    print( 'failed to connect to database' )

try:
    cursor = db.cursor()
except:
    print( 'db.cursor() failed' )

query = '''SELECT * FROM "temps" WHERE read_datetime BETWEEN "2018-03-22" AND 
"2018-03-31"'''

cursor.execute( query )

all = cursor.fetchall()
for thing in all:
    print(thing, '<br>')

db.close()

