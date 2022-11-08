

"""
    This is a script for the temporary extraction of data from the datalogs produced by MESM.
    Will find floats embedded in the logs via regex and create lists of the data for processing using
    typical data science equations.
"""
"""
   * Written By: Tom Mullins
   * Version: 0.20
   * Date Created:  09/19/19
   * Date Modified: 05/31/22
"""
import re, sys, getopt, os, math
from os.path import expanduser
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import astroThemesV85
import sqlite3, re


"""
    Adding functionality to take the file to be processed as an arguement.
"""

def main(argv):
    logFile = ''
    global argVar
    argVar = []

    # Getting the arguements
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])

    # Catching incorrect arguements
    except getopt.GetoptError:
        print('Usage: mesmreader.py -i <inputfile>')
        sys.exit(2)

    for opt, arg in opts:
        # Shows user how to use the script
        if opt == '-h':
            print('Usage: mesmreader.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            logFile = "~/Documents/PythonFiles/MESM/datalogs/" + arg
            argVar.append(arg)
            """
                A function to extract data from a .txt file produced by MESM.
                Takes the datalog's filename as 'datalog'
            """



            def extractor(datalog):



                global temperatures, humidityData, locations, dates, argVar

                # the global lists to be populated by the extractor function
                temperatures = []
                humidityData = []
                locations = []
                dates =[]



                """
                    Connecting to and pulling data from the Databases that MESM now uses as of
                    0.20.
                """

                # Opening the Database passed to the extractor function and setting up the cursor ob.
                connectDB = sqlite3.connect(datalog)
                dbCursor = connectDB.cursor()

                # Selecting the rows we need from the weather table, and then pulling the data
                # from it.
                selectAll = dbCursor.execute("SELECT time, temperature, humidity FROM weather")
                allData = selectAll.fetchall()

                for row in allData:
                    temperatures.append(row[1])
                    humidityData.append(row[2])

                # Starting to pull the date and location from the
                # database name.
                locDate = argVar[0].replace(".db", "")

                # Seperating the location and date from the filename.
                head, sep, tail = locDate.partition('z')
                locations.append(head)
                dateStr = tail

                if locations[0] == "porch":
                    locations[0] = "On My Back Porch"

                dates.append('-'.join(dateStr[i:i+2] for i in range(0, 5, 2 ))) # Making the date more readeable by adding slashes.









                """
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

                        locationMatch = re.search(r'Location: (.*)', line)

                        if locationMatch:
                            locations.append(str(locationMatch.group(1)))

                        dateMatch = re.search(r'Date: (.*)', line)

                        if dateMatch:
                            dates.append(str(dateMatch.group(1)))
                """
                return

            """
            A function that processes data from the extractor function using traditional
            data science methods.
            """

            def processor(temps, humidity):

                # An empty list to be populated for calculating the population variance
                varianceList = []
                global meanTemp, medianTemp, lowestTemp, highestTemp, meanHum, lowestHum, highestHum, medianHumid, hustanDev
                # Getting the simple average temperature. (mean)
                meanTemp = sum(temps)/len(temps)
                print("Simple Average (Mean): %s F" % float("%0.1f" % meanTemp))

                # Calculating the median temperature
                orderedTemp = sorted(temps)

                #print(orderedTemp)
                halfValue = (len(orderedTemp) + 1)/2
                medianTemp = orderedTemp[int(halfValue)]
                print("Median temperature: %s F" % medianTemp)

                # Getting the highest/lowest temps.
                lowestTemp = orderedTemp[0]
                highestTemp = orderedTemp[-1]
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

                # Getting the highest/lowest Humidity.
                lowestHum = orderedHumid[0]
                highestHum = orderedHumid[-1]

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

            # Pulling the data from the text file
            extractor(os.path.expanduser(logFile))
            #print(len(temperatures))
            #print(len(humidityData))
            processor(temperatures, humidityData)


            class App(QMainWindow):



                def __init__(self):
                    super().__init__()

                    #self.setGeometry(0, 0, 0, 0)
                    self.setWindowTitle('MESM Stats')
                    #self.setWindowIcon(QIcon(os.path.expanduser("~/.AstroNinja/Images/Icons/rocket.png")))

                    #self.showMaximized()
                    self.initUI()

                # The the method to setup the window.
                # This is where most of the action happens.
                def initUI(self):

                    #=========================================================================================================
                    # All the functions needed to build a UI for a PyQt5 App
                    #=========================================================================================================

                    # a function for creating and configuring frame items
                    # (a) is the layout that the frame is to be added to
                    # (b) is the first position value
                    # (c) is the second position value
                    # (e) is a toggle for if it is an inner frame

                    def frameBuilder(a, b, c,  d, e ):
                        self.frame = QFrame()

                        self.frame.setFrameShape(QFrame.Box)
                        #self.nextframe.setFixedSize(150, 150)
                        self.frame.adjustSize()
                        a.addWidget(self.frame, b, c)
                        if e == False:
                            global frameLayout
                        frameLayout = QGridLayout()
                        self.frame.setLayout(frameLayout)
                        frameLayout.setHorizontalSpacing(25)
                        a.setColumnMinimumWidth(1, d)



                    # A function that adds verticle margins to layouts
                    # Takes the layout it is to be added to as "a"
                    # "b" and "c" are the x and y dimensions
                    def vert_Spacer(a, b, c):
                        verticalSpacer = QSpacerItem(b, c, QSizePolicy.Maximum, QSizePolicy.Expanding)
                        a.addItem(verticalSpacer, 3, 0)
                        a.addItem(verticalSpacer, 3, 2)


                    # A function for creating scroll objects
                    # gets the tab/location the scroll is to be inserted as location
                    # gets the x and y coordinates as x and y
                    global scroll
                    def scrollBuilder(location, x, y):
                        global scroll
                        scroll = QScrollArea(self)

                        # Creating the style sheet for the scroll bar colors.
                        location.addWidget(scroll, x, y)
                        scroll.setWidgetResizable(True)
                        scrollContent = QWidget(scroll)
                        scroll.layout = QGridLayout(scrollContent)
                        scrollContent.setLayout(scroll.layout)

                        scroll.setWidget(scrollContent)

                    # A function that builds headers
                    # (a) is the message string
                    # (b) is the first position variable
                    # (c) is the second position variable
                    # (d) is the layout that the label is to be added to
                    # (e) is the amount of height given to the header
                    def headerBuild(a, b, c, d, e):

                        self.header = QLabel(a, self)
                        self.header.setAlignment(QtCore.Qt.AlignCenter)
                        self.header.setFixedHeight(e)
                        self.header.setWordWrap(True)
                        self.header.setFont(fontVar)
                        self.header.setStyleSheet('QLabel {background: transparent}')
                        d.addWidget(self.header, b, c)

                    # A quick Qlabel generator
                    # (stringVar) is the string to be displayed
                    # (xCord and yCord) are the coordinates the label is to be placed at
                    # (layout) is the object the label is to be placed in.
                    def genLabel(stringVar,xCord, yCord, layout):

                        self.label = QLabel(stringVar, self)
                        self.label.adjustSize()
                        self.label.setWordWrap(True)
                        self.label.setMaximumWidth(450)
                        self.label.setFont(basicFont)
                        layout.addWidget(self.label, xCord, yCord)

                    # A better function to create label widgets in PyQt5.
                    # Takes the string to be shown as message.
                    # Justification is set with alignment,
                    # font size is set with font
                    # width sets maximum width of the label.
                    # container is where the label is to be placed.
                    def label_maker(message, alignment, font, width, container, xpos, ypos):

                        self.label = QLabel(message, self)
                        self.label.adjustSize()
                        self.label.setWordWrap(True)
                        self.label.setAlignment(alignment)
                        self.label.setMaximumWidth(width)
                        self.label.setFont(font)

                        container.addWidget(self.label, xpos, ypos)


                    def graph_maker(tallies, ylabelString, len,  title, launchers, container, x, y):

                        self.figure = plt.figure(figsize=(len,5))
                        ax = self.figure.add_subplot(111)

                        self.canvas = FigureCanvas(self.figure)

                        container.addWidget(self.canvas, x, y)

                        # Changing the graph colors based on which theme is selected:
                        global bg_color, fg_color, bar_color

                        # creating the color theme
                        bg_color = 'White'
                        fg_color = 'black'
                        bar_color = 'Steelblue'


                        # x-coordinates
                        xItems = len
                        ind = np.arange(xItems)


                        p1 = plt.bar(ind, tallies) #setting the plot

                        for item in p1:
                            item.set_color(bar_color)

                        plt.ylabel(ylabelString, color=fg_color)
                        plt.xlabel('', color=fg_color)
                        plt.title(title, fontsize=17, color=fg_color)
                        plt.xticks(ind, launchers, color=fg_color)
                        if max(tallies) == 0:
                            plt.yticks(np.arange(0, 2), color=fg_color)
                        else:
                            plt.yticks(np.arange(0, max(tallies) + 2, 5.0), color=fg_color)

                        #plt.style.use(u'dark_background')
                        ax.patch.set_facecolor(bg_color)
                        #ax.autoscale(enable=True)
                        ax.tick_params(axis='x', labelsize=8)
                        self.figure.patch.set_facecolor(bg_color)

                        # Adding the totals to the bars
                        for index,data in enumerate(tallies):
                            plt.text(x=index , y =data-data , s=f"{data}" , fontdict=dict(fontsize=8, ha='center', va='bottom', color=bg_color))
                        self.canvas.draw()


                    # Set the central widget
                    central_widget = QWidget(self)          # Create a central widget
                    self.setCentralWidget(central_widget)
                    grid_layout = QGridLayout()         # Create a QGridLayout
                    central_widget.setLayout(grid_layout)   # Set Layout to central widget

                    # Setting fonts
                    fontVar = QFont("Noto Sans", 25)        # Create a QFont instance
                    fontVar.setBold(True)

                    smallerHeader =  QFont("Noto Sans", 17)
                    smallerHeader.setBold(True)

                    welcomeFont = QFont("Noto Sans", 15)                                # A smaller Font
                    welcomeFont.setBold(False)

                    basicFont = QFont("Noto Sans", 13)                                # An even smaller Font
                    basicFont.setBold(False)


                    # Creating the tabs
                    self.tabs = QTabWidget()
                    self.mainTab = (QWidget())

                    # Setting the theme
                    astroThemesV85.spacexTabs(self.mainTab)

                    self.tabs.addTab(self.mainTab, "Graphs")

                    # Creating the first tab
                    self.mainTab.layout = QGridLayout()


                    # Creating a Welcome Header
                    message = "Stats for {}, {}".format(locations[0], dates[0])
                    headerBuild(message, 0, 1, self.mainTab.layout, 50)

                    # Building the scroll container the graphs will go into.
                    scrolly = scrollBuilder(self.mainTab.layout, 1, 1)

                    # Creating the lists of data to be used in the graphs
                    statLabels = ('Average\nTemperature', 'Median\nTemperature', "Lowest\nTemperature", "Highest\nTemperature")
                    tempNums = (float("%0.1f" % meanTemp), medianTemp, lowestTemp, highestTemp)

                    # Creating the first graph.
                    graph_maker(tempNums, "Degrees Fahrenheit", 4, "Temperature Data\n", statLabels, scroll.layout, 0, 1)

                    # Creating the lists of data to be used in the second graph
                    humLabels = ('Average\nHumidity', 'Median\nHumidity', 'Lowest\nHumidity', 'Highest\nHumidity', 'Deviation')
                    humNums = (float("%0.1f" % meanHum), medianHumid, lowestHum, highestHum, hustanDev)

                    # Creating the second Graph
                    graph_maker(humNums, "Percentage", 5, "Humidity Data\n", humLabels, scroll.layout, 2, 1)

                    # Adding Horizontal spacers inbetween frame items
                    #horizSpacer = QSpacerItem(50, 50, QSizePolicy.Maximum)
                    #scroll.layout.addItem(horizSpacer, 1, 1)

                    # Adding a verticle spacer
                    vert_Spacer(scroll.layout, 250, 250)

                    self.mainTab.setLayout(self.mainTab.layout)
                    grid_layout.addWidget(self.tabs)

                    self.statusBar()
                    self.showMaximized()

            app = QApplication(sys.argv)
            ex = App()
            sys.exit(app.exec_())

if __name__ == '__main__':
    main(sys.argv[1:])

    #sys.exit(app.exec_())
