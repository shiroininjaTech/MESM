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
   * Version: 0.10
   * Date Created:  04/20/19
   * Date Modified: 04/23/19
"""
import sys, os
import Adafruit_DHT
import time
import RPi.GPIO as GPIO

# The global variables to be used by the program.
# minuteCount logs minutes since initialization, acting as a crude way to track time w/o networking.
minuteCount = 0
# When 60 minutes are counted, hourCount is advanced.
hourCount = 0

# Opening the text file for recording readings from the sensors.
# Opened in Append mode.
recordedData = open('datalog.txt', 'a')


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
    converts it, and saves it to datalog.txt.

    It then increments minuteCount and hourCount as necessary.
"""
def main():

    global minuteCount, hourCount

    # Opening the text file for recording readings from the sensors.
    # Opened in Append mode.
    recordedData = open('datalog.txt', 'a')

    # reading data from sensor.
    humidity, temperature =  Adafruit_DHT.read_retry(11, 24)
    # converting to fehrenheit
    temperatureConverted = fahrenheitConverter(temperature)

    # The info to be written to datalog.txt
    roughDraft = "\n T+ {} Hrs, {} Minutes\n Temp: {} F\n Humidity: {} %\n\n".format(hourCount, minuteCount, temperatureConverted, humidity)

    recordedData.write(roughDraft)
    recordedData.close()

    # Incrementing the time counters.
    minuteCount += 1
    # if minuteCount reaches 60, increment hourCount by 1 and reset minuteCount to 0
    if minuteCount == 60:
        hourCount += 1
        minuteCount = 0

    return

# Run main until 6 hours passes
while True:

    input_state = GPIO.input(12)

    main()

    if input_state == False:
        os.system('sudo shutdown -r now')

    time.sleep(60) # wait 60 seconds between runs.
