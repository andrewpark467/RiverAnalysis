

import requests,json
from datetime import datetime as dt
from datetime import timedelta 
import pandas as pd




#Lets open up our files



testDictOne = { 
    "DATETIME" : [
        "2022-01-01 00:00:00-07:00", 
        "2022-01-01 00:15:00-07:00" ,  
        "2022-01-01 00:30:00-07:00"  , 
        "2022-01-01 00:45:00-07:00"   ,
        "2022-01-01 01:00:00-07:00",
    ],
    "CFS1" : [100,100,100,100,100]
}

testDictTwo = { 
    "DATETIME" : [
        "2022-01-01 00:00:00-07:00", 
        "2022-01-01 00:10:00-07:00" ,  
        "2022-01-01 00:30:00-07:00"  , 
        "2022-01-01 00:40:00-07:00"   ,
        "2022-01-01 01:00:00-07:00",
    ],
    "CFS2" : [200,200,200,200,200]
}

dfOne,dfTwo = pd.DataFrame.from_dict(testDictOne),pd.DataFrame.from_dict(testDictTwo)
dfOne["DATETIME"] = pd.to_datetime(dfOne["DATETIME"])
dfTwo["DATETIME"] = pd.to_datetime(dfTwo["DATETIME"])


tmp = pd.merge_asof(dfOne,dfTwo, on= "DATETIME" , tolerance=pd.Timedelta('1min') )

print(tmp)


tmp["DIFF"] = tmp["CFS1"] - tmp["CFS2"]

print(tmp)