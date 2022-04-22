"""
Author: Andrew Park
Date: 4/22/2022
Purpose:
    Perform stats on data
"""
#create Paths
mainPath = "D:/rainEffect"
dataPath = "%s/data" % (mainPath)

from matplotlib.pyplot import title
from riverFunctions import *
from pandas.plotting import scatter_matrix
import seaborn as sns

ogden,eggs,canyonExit = openDataFile("10137000"), openDataFile("10136500"),openDataFile("10136600")
ogden["CFS1"],eggs["CFS2"],canyonExit["CFS3"] = ogden["CFS"],eggs["CFS"],canyonExit["CFS"]

merged_df = pd.merge_asof(ogden, eggs, on = "DATETIME" , tolerance=pd.Timedelta('1min') )
merged_df = merged_df.drop(columns=['CFS_x', 'CFS_y'])

merged_df2 = pd.merge_asof(ogden, canyonExit, on = "DATETIME" , tolerance=pd.Timedelta('1min') )
merged_df2 = merged_df2.drop(columns=['CFS_x', 'CFS_y'])

plt.figure(figsize=(20,20))
plt.title("Ogden vs Highest Measuremente site")
plt.scatter(merged_df["CFS1"] , merged_df["CFS2"] , marker = ".")
plt.xlabel("Ogden")
plt.ylabel("Upper Site")
plt.xlim(0,500),plt.ylim(0,500)
plt.savefig("%s/vs1.jpg" %(dataPath))

plt.figure(figsize=(20,20))
plt.title("Ogden vs Canyon Exit site")
plt.scatter(merged_df2["CFS1"] , merged_df2["CFS3"] , marker = ".")
plt.xlabel("Ogden")
plt.ylabel("Canyon Exit Site")
plt.xlim(0,500),plt.ylim(0,500)
plt.savefig("%s/vs2.jpg" %(dataPath))