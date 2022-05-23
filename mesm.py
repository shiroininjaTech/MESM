#!/usr/bin/python3

"""
   This is the main script for the MESM system intended for the Raspberry pi zero
   MESM stands for Mobile Environmental Sensor Module.
   Using the DH11 humidity/temperature sensor, and future sensing abilities, the
   unit is meant to be worn on a backpack, etc while hiking and will measure
   atmospheric conditions and record the data using Python.

"""
"""
   * Written By: Tom Mullins
   * Version: 0.20
   * Date Created:  04/20/19
   * Date Modified: 05/23/22
"""
import sys, os
import Adafruit_DHT
import time
import RPi.GPIO as GPIO
import sqlite3
import traceback

# The global variables to be used by the program.
# minuteCount logs minutes since initialization, acting as a crude way to track time w/o networking.
minuteCount = 0
# When 60 minutes are counted, hourCount is advanced.
hourCount = 0

# Setting up the gpio for the shutdown Button
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)


"""
    A Function that converts the Celcius temperature from the DH11 to fehrenheit
    returns the temperature.
"""

def fahrenheitConverter(x):
    converted = x*9/5+32
    return converted

"""
    The main function for MESM that reads the data from the sensor,
    converts it, and saves it to a SQLite3 Database.

    It then increments minuteCount and hourCount as necessary.
"""
def main():

    global minuteCount, hourCount

    """
        Adding database functionality to replace using just a text file.
    """


    # creating the database
    conn = sqlite3.connect('recorded_data.db')




    #connecting to the database.
    c = conn.cursor()

    # Creating the temperature table
    c.execute("""
            CREATE TABLE IF NOT EXISTS weather
            ([_id] INTEGER PRIMARY KEY, [time] TEXT NOT NULL, [temperature] REAL, [humidity] REAL)
            """)

    conn.commit()



    # reading data from sensor.
    humidity, temperature =  Adafruit_DHT.read_retry(11, 24)
    # converting to fehrenheit
    temperatureConverted = fahrenheitConverter(temperature)

    # Creating a time string, for simplicity
    hourMin = "{}:{}".format(hourCount, minuteCount)

    # A SQL inseart as a string so I can use parameters
    dataInsert = """
            INSERT OR REPLACE INTO weather
                VALUES
                (null, ?, ?, ?)
            """

    # Creating a list of the data to be inserted to used a parameter.
    gatheredData = (hourMin, temperatureConverted, humidity)

    # The actual SQL insert.
    c.execute(dataInsert, gatheredData)
    conn.commit()
    c.close()

    # Incrementing the time counters.
    minuteCount += 1
    # if minuteCount reaches 60, increment hourCount by 1 and reset minuteCount to 0
    if minuteCount == 60:
        hourCount += 1
        minuteCount = 0

    return

# Run main until 6 hours passes
try:

    while True:

        input_state = GPIO.input(12)

        main()

        if input_state == False:
            os.system('sudo shutdown -r now')

        time.sleep(60) # wait 60 seconds between runs.

except:
     errorFile = open('MESMreport.txt', 'w')
     errorFile.write(traceback.format_exc())
     errorFile.close()
     print('The traceback info was written to MESMreport.txt')
finally:
    GPIO.cleanup()
