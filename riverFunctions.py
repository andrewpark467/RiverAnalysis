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

#import
import requests,json
from datetime import datetime as  dt
from datetime import timedelta as td 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import diff

def authenticate():
    #Example ket KuNzf2GTrQXSpj2mwJb4JovQt7qeNJ0ASsfn4m5UrK
    key = "KuNzf2GTrQXSpj2mwJb4JovQt7qeNJ0ASsfn4m5UrK"
    url = " https://api.synopticdata.com/v2/auth?&apikey=%s" % (key)
    print("Requesting auth key/token...")
    r = requests.get(url)
    if r.status_code != 200:
        print("Auth service failed with status code: %s") % (r.status_code)
    print("Auth key/token request successful... ")
    token = r.json()
    return(token["TOKEN"])

#build function that grabs synoptic data from station, start time, and end time 
#collects, groom, and places data in simple json txt file.
def grabData(STID,timeOne,timeTwo):
    print("Now working on station %s " %(STID))
    #now we can build a url to start collecting data
    #time format == YYYYMMDDHHMM , UTC time
    mainURL = "https://api.synopticdata.com/v2/stations/timeseries?"
    buildURL = "&token=%s&stid=%s&vars=precip_accum_one_hour&start=%s&end=%s&units=english&output=json" %(authenticate(), STID, timeOne ,timeTwo)
    url = "%s/%s" %(mainURL,buildURL)
    r = requests.get(url)
    if r.status_code != 200:
        print("Request failed %s" %(r.status_code) ) 
    data = r.json()
    

    masterDict = {
        "DATETIME" : data["STATION"][0]["OBSERVATIONS"]["date_time"], 
        "PRECIP"   : [] 
    }

    for i in data["STATION"][0]["OBSERVATIONS"]["precip_accum_one_hour_set_1"]:
        if i != None:
            masterDict["PRECIP"].append(float(i))
        else:
            masterDict["PRECIP"].append(np.nan)

    with open("%s/%s.txt" % (dataPath, STID), "w" ) as saveFile:
        json.dump(masterDict, saveFile)
    print("-------------------------------------------------------")
        
def grabRiverData(name,stid,timeOne,timeTwo):
    #time format is YYYY-MM-DDTHH:MM-0600 maybe 700 if dst? 
    #x = input("Did you enter timeformat as  YYYY-MM-DDTHH:MM-0600? y/n: ")
    #if x != "y":
    #    exit()
 
    print("Now gathering data for river station %s, STID: %s" %(name, stid))
    firstURL = "https://waterservices.usgs.gov/nwis/iv/?format=json&sites={}".format(stid)
    
    secondURL = "&startDT=%s&endDT=%s&parameterCd=00060&siteStatus=all" %(timeOne,timeTwo)
    url = "%s%s" %(firstURL,secondURL)
    print(url)

    print("Now grabbing data from USGS at url: %s" %(url))

    r = requests.get(url)
    print("Status Code: %s" % (r.status_code)) 

    if r.status_code != 200:
        print("Requests failed... status code: %s" %(r.status_code))

    #Grab JSON requests and save into local dictionary.     
    data = r.json()

    #Grab info we want. 
    saveDict = {"DATETIME" : [] , "CFS" : []}

    for i in data["value"]["timeSeries"][0]["values"][0]["value"]:
        saveDict["DATETIME"].append(i["dateTime"])
        #if i["value"] == None:
        #    saveDict["CFS"].append(np.nan)
        if float(i["value"]) >= 0:
            saveDict["CFS"].append(float(i["value"]))
        else:
            saveDict["CFS"].append(np.nan)


    with open("%s/%s.txt" % (dataPath, stid) , "w") as finalFile:
        json.dump(saveDict, finalFile)

    print("success, data saved...")

def openDataFile(i):
    with open("%s/%s.txt" %(dataPath, i) , "r" ) as openFile:
        data = json.load(openFile)
        data["DATETIME"] = pd.to_datetime(data["DATETIME"], utc=True)
        return pd.DataFrame.from_dict(data)


#Now lets create a function to look at river difference, specifically, I-84 "upperwebber" vs Ogden whitewater park
#delta_h = h2 - h1 where:
    #h2 = ogden park
    #h1 = upper Webber
def createDifference( stationTupleOne, stationTupleTwo):
    stationOneName,stationOneID = stationTupleOne[0],stationTupleOne[1]
    stationTwoName,stationTwoID = stationTupleTwo[0],stationTupleTwo[1]
    #lets try to use pandas....
    dictOne = openDataFile("%s" %(stationOneID))   #CFS
    dictTwo = openDataFile("%s" %(stationTwoID))    #CFS
    #-----------------------------------------
    dfOne = pd.DataFrame.from_dict(dictOne)
    dfOne["CFS1"] = dfOne["CFS"]
    dfTwo = pd.DataFrame.from_dict(dictTwo)
    dfTwo["CFS2"] = dfTwo["CFS"]

    dfOne["DATETIME"] = pd.to_datetime(dfOne["DATETIME"], utc=True)
    dfTwo["DATETIME"] = pd.to_datetime(dfTwo["DATETIME"],utc=True)
    merged_df = pd.merge_asof(dfOne,dfTwo, on= "DATETIME" , tolerance=pd.Timedelta('1min') )

    merged_df["DIFF"] = merged_df["CFS1"] - merged_df["CFS2"]

    return merged_df

#Now we can open all four files, and go to town
#stid is a list or tuple of all file names
def finalGroom(stations,timeXOne, timeXTwo):
    print("Opening station files.....")
    #totalList = ("GATU1" , "KHIF" , "KOGD", "10137000")
    gatu = openDataFile("GATU1")       #precip
    hill  = openDataFile("KHIF")       #precip
    ogden = openDataFile("KOGD")       #precip
    weber = openDataFile("10137000")   #CFS
    #echo = openDataFile("10132000")    #CFS
    upperWeber = openDataFile("10136600")    #CFS
    eggs = openDataFile("10136500")    #cfs
    difference = createDifference(("Ogden" , "10137000"), ("UpperWever" , "10136600"))



    print("-------------------------------------------")
    print("files opened.. plotting data ")
    # create figure and axis objects with subplots()
    fig,ax = plt.subplots(figsize=(20,10))
    ax.set_title("Ogden White Water Park")
    # make a plot
    ax.plot(weber["DATETIME"] , weber["CFS"], color="#0031B1", linestyle = "-" , label = "Ogden")
    #ax.plot(echo["DATETIME"] , echo["CFS"], color="#B4BDFF", linestyle = "0, (5, 10)")
    ax.plot(upperWeber["DATETIME"] , upperWeber["CFS"], color="#4F7CF2", linestyle = "dashed", label = "84 exit")
    ax.plot(eggs["DATETIME"] , eggs["CFS"], color="#96B3FF", linestyle = "dashdot", label = "Above Eggs")

    # set x-axis label
    ax.set_xlabel("time",fontsize=14)
    # set y-axis label
    ax.set_ylabel("CFS",color="red",fontsize=14)
    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(gatu["DATETIME"] ,  gatu["PRECIP"],color="#676767",marker="." , linestyle = "none" )
    ax2.plot(ogden["DATETIME"] , ogden["PRECIP"],color="#1E0303",marker=".", linestyle = "none")
    ax2.plot(hill["DATETIME"] ,  hill["PRECIP"],color="#1E0303",marker=".", linestyle = "none")
    ax2.set_ylabel("PRECIP",color="black",fontsize=14)
    if len(timeXOne) and len(timeXTwo) > 1:
        ax.set_xlim([ dt.strptime(timeXOne, "%Y-%m-%dT%H:%M") , dt.strptime(timeXTwo, "%Y-%m-%dT%H:%M") ])
       #ax.set_xlim([ datetime.date(2014, 1, 26)               , datetime.date(2014, 2, 1)               ])
    ax2.set_ylim(0.05, 0.50)
    ax.legend()
    ax.grid()
    
    plt.savefig("%s/weber.jpg" % (dataPath))
    print("Image created.")




def diffPlot(stations,timeXOne, timeXTwo):
    print("Opening station files.....")
    #totalList = ("GATU1" , "KHIF" , "KOGD", "10137000")
    #gatu = openDataFile("GATU1")       #precip
    #hill  = openDataFile("KHIF")       #precip
    #ogden = openDataFile("KOGD")       #precip
    weber = openDataFile("10137000")   #CFS
    #echo = openDataFile("10132000")    #CFS
    #upperWeber = openDataFile("10136600")    #CFS
    #eggs = openDataFile("10136500")    #cfs
    difference = createDifference(("Eggs" , "10136500"),("Ogden" , "10137000"))



    print("-------------------------------------------")
    print("files opened.. plotting data ")
    # create figure and axis objects with subplots()
    fig,ax = plt.subplots(figsize=(20,10))
    ax.set_title("Ogden White Water Park")
    # make a plot
    ax.plot(weber["DATETIME"] , weber["CFS"], color="#0031B1", linestyle = "-" , label = "Ogden")
    #ax.plot(echo["DATETIME"] , echo["CFS"], color="#B4BDFF", linestyle = "0, (5, 10)")
    #ax.plot(upperWeber["DATETIME"] , upperWeber["CFS"], color="#4F7CF2", linestyle = "dashed", label = "84 exit")
    #ax.plot(eggs["DATETIME"] , eggs["CFS"], color="#96B3FF", linestyle = "dashdot", label = "Above Eggs")
  

    # set x-axis label
    ax.set_xlabel("time",fontsize=14)
    # set y-axis label
    ax.set_ylabel("CFS",color="red",fontsize=14)
    # twin object for two different y-axis on the sample plot
    ax2=ax.twinx()
    # make a plot with different y-axis using second axis object
    ax2.plot(difference["DATETIME"] , difference["DIFF"], color="black", linestyle = "--", label = "weber_eggs difference")

    if len(timeXOne) and len(timeXTwo) > 1:
        ax.set_xlim([ dt.strptime(timeXOne, "%Y-%m-%dT%H:%M") , dt.strptime(timeXTwo, "%Y-%m-%dT%H:%M") ])
       #ax.set_xlim([ datetime.date(2014, 1, 26)               , datetime.date(2014, 2, 1)               ])
    
    ax.legend(loc=1)
    ax2.legend(loc=2)
    ax2.grid()
    
    plt.savefig("%s/weber_diff.jpg" % (dataPath))
    print("Image created.")
