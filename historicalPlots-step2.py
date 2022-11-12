#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 08:38:52 2022

@author: DeepShadow


This code expects a list of folders named as "topNN" with "NN" currently set to 20, 50 and 100, created by historicalPlots-step2.py 
In each folder, it reads the data from all the CSV file in the form:
    YYYY-MM-DD tournyDinoTop NN.csv
with: 
    YYYY-MM-DD Year, Month and Day (ISO Format) when the data were downloaded
    NN value currently set via "dinoSteps"
Examples:
    2022-05-07 tournyDinoTop 20.csv
    2022-10-29 tournyDinoTop 20.csv

The main loop creates the summary usage tables at "dinoSteps" thresholds, currently set to 20, 50 and 100. 
Each file is named as 
    YYYY-MM-DD HH.MM.SS topNN.csv
with
    YYYY-MM-DD Year, Month and Day (ISO Format) when the the summary table was created
    HH.MM.SS Hour, minutes and seconds when the the summary table was created
    NN value currently set via "dinoSteps"
Example:
    2022-10-30 11.39.25 top20.csv

The contents of the CSV file are arranged as: 

    Dino	v 2022-05-07	v 2022-05-29	v 2022-06-08
    Refrenant	92	95	93
    Indotauru	86	68	74
    Ankyloslux	84	92	94

First row: "Dino", then version of the downloaded data (i.e. when the data were downloaded)
Firsr column: "Dino", then the names of the most popular dinos. 


These data can be used to display historical usage graphs in your preferred program 


"""

dinoSteps = [20, 50, 100] 
tournamentID = 'PVP'

for dinoSelection in dinoSteps:


    dirToCheck = 'top'+str(dinoSelection)
    # other possible values are 'top20' and 'top50'
    
    
    
    
    # select only rows above this threshold to remove cluttering
    minThreshold = 25; 
    
    
    import os
    from sys import platform
    # import glob
    
    import pandas as pd
    import numpy as np
    
    
    from ast import literal_eval
    from itertools import chain
    
    from datetime import datetime
    
    
    
    if platform == "darwin":
        print('Mac OS X')
        os.chdir("/Users/Coding/python/Dino/history")
    
    elif platform == "win32":
        print("Windows")
        os.chdir("D:\Coding\python\Dino\history")

    
    
    os.chdir(dirToCheck)
    
    a = os.listdir()
    b = list(filter(lambda k: 'tournyDinoTop' in k, a))
    b.sort()
    
    
    data = pd.DataFrame()
    
    for i in b:
        print(i)
        
        t = i.find(" ")
        dataDate = "v " + i[:t]
    
        dinoData = pd.read_csv(rf'{i}')
        dinoData = dinoData[["Dino", "Count%"]]
        
        
        
        if (data.empty):
            # nothing to do the first time 
            data = dinoData
            data = data.rename(columns={'Dino':'Dino', 'Count%':dataDate})
            
            
        else:
            # empty column
            data[dataDate]= 0 # float("NaN")
        
            for dino in dinoData["Dino"]:
                currentCount = float(dinoData [dinoData['Dino']==dino]["Count%"])
                # print (dino)
    
                if (dino not in data['Dino'].tolist()):
                    # DEPRECATED METHOD
                    # data[dataDate][data["Dino"]==dino] = currentCount
    
                    #             else:
                    # data.shape[1] contains the current number of columns in the dataframe
                    list1 = list()
                    list1.append(dino)
                    for x in range (data.shape[1]-1):
                        list1.append(float("NaN"))
    
                    newDino = pd.Series(list1, index = data.columns)   
                    newDino = pd.DataFrame(newDino)
                    newDino = newDino.transpose()
                    
                    data = pd.concat([data, newDino])
                    #                 data = data.append(newDino, ignore_index=True)
                    
                data.loc[data["Dino"]==dino, dataDate] = currentCount                
                    
                
    # FINAL CLEANUP
    
    
    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H.%M.%S ")
    
                
    data2 = data[data.columns[1:data.shape[1]]]
    selection = (data2 >= minThreshold).any(1)
               
    
    data3 = data[selection]
    
        
    os.chdir('..')
    filename = dt_string + dirToCheck + '.csv'
    data3.to_csv(filename, index=False)
    print (filename + ' saved.')




























