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

path = "/Users/esthersui/Desktop/DIGI/sharedFiles/"

stockColNames = ["date", "tradeVol", "trade", "openPrice","highestPrice","lowestPrice", "closePrice","dif","transaction" ]

s2330 = pd.read_csv(path+ "stockPrices/upstream/2330.csv", names = stockColNames)

twCase = pd.read_csv(path+"確診人數統計/台灣確診人數統計_E.txt",delimiter = '\t')

#case data cleanup
useCase = twCase.loc[29:561]
useCase["date"] = pd.to_datetime(useCase["date"]).dt.date
useCase = useCase.drop("ID", axis = 1)

#stock datetime cleanup
s2330 = s2330.drop(index = 0)
s2330 = s2330.dropna()
d = s2330["date"]
for i in range(len(s2330)):
    d.iloc[i]=d.iloc[i].replace(d.iloc[i][0:3], str(int(d.iloc[i][0:3]) + 1911))
d=pd.to_datetime(d,format='%Y/%m/%d').dt
s2330['date'] = pd.to_datetime(s2330['date']).dt.date

#combining stock price and cases data
combine = pd.merge(useCase, s2330, on =["date"], how = "outer")
combine = combine.replace(",", '')
combine = combine.dropna()
date = np.array(combine[1:])[:,0]
stock = np.array(combine[1:])[:,29].astype(float)

#stock plot
degrees = 70
plt.figure()
ax = plt.gca()
ax.set_ylim(0, max(stock)+20)
plt.xlabel("Date")
plt.ylabel("Stock Price")
ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
ax.xaxis.set_major_locator(mdates.DayLocator(1))
plt.plot(list(date) ,stock,color = "black")
plt.xticks(rotation = degrees)
#plt.savefig('2330.tiff')


#case/stockPlot
case = np.array(combine[1:])[:,2].astype(float)
plt.plot(list(date),case,color = "blue")
plt.show()














