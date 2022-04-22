"""
Author: Andrew Park
Date: 4/15/2022
Purpose:
    Check to see rain impacts and CFS rise for Station 10137000 Ogden/Wever River
    1) Need to grab data from Synoptic and USGS
    2) Groom data
        a) put into json folder with hourly datetime
    3) plot data
"""
#create Paths
mainPath = "D:/rainEffect"
dataPath = "%s/data" % (mainPath)

from riverFunctions import *

surfaceStationList = ("GATU1" , "KHIF" , "KOGD")
riverStationList = ("10137000")
totalList = ("GATU1" , "KHIF" , "KOGD", "10137000")

'''
for i in surfaceStationList:
    grabData(i,"202201010000","202204221200")

grabRiverData("weber"   , "10137000","2022-01-01T00:00-0600" , "2022-04-22T12:00-0600" )
grabRiverData("echo"    , "10132000","2022-01-01T00:00-0600" , "2022-04-22T12:00-0600" )
grabRiverData("Weber_84", "10136600","2022-01-01T00:00-0600" , "2022-04-22T12:00-0600" )
grabRiverData("eggs"    , "10136500","2022-01-01T00:00-0600" , "2022-04-22T12:00-0600" )
grabRiverData("eggs"    , "10136500","2022-01-01T00:00-0600" , "2022-04-22T12:00-0600" )
'''

#finalGroom(totalList, "2022-04-20T12:00" , "2022-04-22T12:00" )
#diffPlot(totalList, "2022-04-11T12:00" , "2022-04-22T12:00" )


