

"""
    This is a script for the temporary extraction of data from the datalogs produced by MESM.
    Will find floats embedded in the logs via regex and create lists of the data for processing using
    typical data science equations.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.10
   * Date Created:  09/19/19
   * Date Modified: 09/26/19
"""
import re, sys, os, math
from os.path import expanduser

"""
    A function to extract data from a .txt file produced by MESM.
    Takes the datalog's filename as 'datalog'
"""

# the global lists to be populated by the extractor function
temperatures = []
humidityData = []

def extractor(datalog):

    global temperatures, humidityData

    # Opening the text file
    with open(datalog) as recordedData:
        # iterating through each line in the file.
        for line in recordedData:
            tempMatch = re.search(r'Temp: (.*) F', line)  # Using regex to search for the characters

            # if found, convert found object to float and add to list.
            if tempMatch:
                foundTemp = float(tempMatch.group(1))
                temperatures.append(foundTemp)

            humidityMatch = re.search(r'Humidity: (.*) %', line)

            if humidityMatch:
                foundHumidity = float(humidityMatch.group(1))
                humidityData.append(foundHumidity)
    return

"""
    A function that processes data from the extractor function using traditional
    data science methods.
"""

def processor(temps, humidity):

    # An empty list to be populated for calculating the population variance
    varianceList = []

    # Getting the simple average temperature. (mean)
    meanTemp = sum(temps)/len(temps)
    print("Simple Average (Mean): %s F" % float("%0.1f" % meanTemp))

    # Calculating the median temperature
    orderedTemp = sorted(temps)
    #print(orderedTemp)
    halfValue = (len(orderedTemp) + 1)/2
    medianTemp = orderedTemp[int(halfValue)]
    print("Median temperature: %s F" % medianTemp)

    # Calculating population variance
    for i in orderedTemp:
        varianceList.append((i - meanTemp)**2)

    # Adding all of varianceList's items and dividing them
    # by the number of measurements, giving the population variance.
    tempVar = sum(varianceList)/len(orderedTemp)
    print("Population Variance: %s " % float("%0.2f" % tempVar))

    # Calculating the Population Standard Deviation.
    stanDev = math.sqrt(tempVar)
    print("Pop. Standard Deviation: %s\n" % float("%0.2f" % stanDev))

    # Now for processing data on Humidity.
    # An empty list to be populated for calculating the population variance
    humidVariance = []

    # Getting the simple average temperature. (mean)
    meanHum = sum(humidity)/len(humidity)
    print("Simple Average Humidity(Mean): %s" % float("%0.1f" % meanHum))

    # Calculating the median temperature
    orderedHumid = sorted(humidity)
    #print(orderedTemp)
    halfHumid = (len(orderedHumid) + 1)/2
    medianHumid = orderedHumid[int(halfHumid)]
    print("Median Humidity: %s " % medianHumid)

    # Calculating population variance
    for i in orderedHumid:
        humidVariance.append((i - meanHum)**2)

    # Adding all of varianceList's items and dividing them
    # by the number of measurements, giving the population variance.
    humidVar = sum(humidVariance)/len(orderedHumid)
    print("Population Variance: %s " % float("%0.2f" % humidVar))

    # Calculating the Population Standard Deviation.
    hustanDev = math.sqrt(humidVar)
    print("Pop. Standard Deviation: %s" % float("%0.2f" % hustanDev))
    return

extractor(os.path.expanduser('datalogs/datalog.txt'))
#print(len(temperatures))
#print(len(humidityData))
processor(temperatures, humidityData)
