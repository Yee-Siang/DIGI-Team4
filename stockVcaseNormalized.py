#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 23:00:18 2021

@author: esthersui
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 31 15:35:22 2021

@author: esthersui
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn import preprocessing

path1 = "/Users/esthersui/Desktop/DIGI/sharedFiles/"

stockColNames = ["date", "tradeVol", "trade", "openPrice","highestPrice","lowestPrice", "closePrice","dif","transaction" ]

s2330 = pd.read_csv(path1+ "stockPrices/upstream/2330.csv", names = stockColNames)

path = "/Users/esthersui/Desktop/DIGI/sharedFiles/確診人數統計/"
taiwan = pd.read_excel(path+'台灣確診人數統計.xlsx')
america = pd.read_excel(path+'美國確診人數統計.xlsx')
america= america.rename(columns = america.iloc[0])
america= america.drop(index = 0)
europe = pd.read_excel(path +'歐洲確診人數統計.xlsx')
europe = europe.rename(columns = europe.iloc[0])
europe = europe.drop(index = 0)
countries = ["taiwan",  "america", "europe"]


upstreamCorps = ['2330',"2317", "2379", "2388","2454", "3008"]
upStocks = pd.DataFrame()


#case data cleanup
useCase = america
useCase["date"] = pd.to_datetime(useCase["date"]).dt.date
useCase = useCase.drop("ID", axis = 1)
upstream_normed = []
for corp in upstreamCorps:
    sTemp = pd.read_csv(path1+ "stockPrices/upstream/"+corp+".csv", names = stockColNames)
    sTemp = sTemp.drop(index = 0)
    sTemp = sTemp.dropna()
    d = sTemp["date"]
    print(corp)
    for i in range(len(sTemp)):
        d.iloc[i]=d.iloc[i].replace(d.iloc[i][0:3], str(int(d.iloc[i][0:3]) + 1911))
    d=pd.to_datetime(d,format='%Y/%m/%d').dt
    sTemp['date'] = pd.to_datetime(sTemp['date']).dt.date
    
    locals()["dataStock" + str(corp)] = sTemp
    
  
    if corp == "2330":
        combine = pd.merge(useCase, sTemp, on =["date"], how = "outer")
        combine = combine.replace(",", '')
        combine = combine.dropna()
    else:
        combine = pd.merge(combine, sTemp, on =["date"], how = "outer")
        combine = combine.replace(",", '')
        combine = combine.dropna()
    
    
for i in range(0,6):
    locals()["stock"+str(upstreamCorps[i])] = np.array(combine[1:])[:,11+i*8].astype(float)
    print(i)

    
date = np.array(combine[1:])[:,3]
#combining stock price and cases data

degrees = 70
plt.figure()
ax = plt.gca()
plt.xlabel("Date")
plt.ylabel("Stock Price")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
ax.xaxis.set_major_locator(mdates.DayLocator(1))
#plt.xticks(rotation = degrees)
fig, ax_left = plt.subplots()
ax_left.set_xlabel("normalized stock")
ax_left.tick_params(axis='x', rotation = degrees)
from sklearn import preprocessing


#stock plot
for i in range (0,5):
    x_array = np.array(locals()["stock"+str(upstreamCorps[i])])
    normalized_arr = preprocessing.normalize([x_array])
    stockInput = normalized_arr.transpose()
    lns1 = ax_left.plot(list(date), stockInput)

ax_right = ax_left.twinx()
ax_left.set_xlabel("new cases")
#case/stockPlot
case = np.array(combine[1:])[:,9].astype(float)
lns2 = ax_right.plot(list(date),case,color = "blue")

ax_left.legend(['2330',"2317", "2379", "2388","2454", "3008"], loc = "upper left") 
ax_right.legend(["newCases"], loc = "upper right")  

plt.show()









