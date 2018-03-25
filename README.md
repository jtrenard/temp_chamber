# temp_chamber

Original sample code and configuration came from:
http://www.allaboutcircuits.com/projects/transmit-temperature-with-raspberry-pi/

sudo apt-get install python-smbus i2c-tools

Test with command:
sudo i2cdetect -y <x>
Where <x> is the i2c bus number.

SQLite3 Database:

  Table: temps
  | read_datetime |  readings |
