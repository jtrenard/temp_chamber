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

db = sqlite3.connect('./env_state.db' )

cursor = db.cursor()
query = '''SELECT * FROM temps WHERE read_datetime >= DATEADD( n, -2, 
    GETDATE())'''

cursor.execute( query )

db.close()
