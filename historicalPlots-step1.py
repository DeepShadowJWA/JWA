#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 08:38:52 2022

@author: DeepShadow


This code expects a list of folders named as "YYYY-MM-DD PVP" with:
    YYYY-MM-DD Year, Month and Day (ISO Format) when the data were downloaded
Examples:
    2022-10-29 PVP
    2022-09-28 PVP

Each folder contains two files obtained through Lullatsch's JWA Protocol Decoder:
    - xxxxxxxxxxxx_dino_boosts.csv
    - yyyyyyyyyyyy_dino_teams.csv

The main loop creates the dino usage tables at "dinoSteps" thresholds, currently set to 20, 50 and 100. 

These data will be used by the historicalPlots-step2.py routine

Once run, the folders should be renamed to remove "PVP" (I use "PVdone"). 
The saved data will be reused so no need to calculate them again. 

Folder names in lines 55/59 should be adjusted to match the machine currently used


"""

dinoSteps = [20, 50, 100] 
tournamentID = 'PVP'

for dinoSelection in dinoSteps:

#    dinoSelection = 100 # 'all' # or any number you want to select

    
    
    
    import os
    from sys import platform
    # import glob
    
    import pandas as pd
    
    from ast import literal_eval
    from itertools import chain
    
    
    
    
    if platform == "darwin":
        print('Mac OS X')
        os.chdir("/Users/Coding/python/Dino/history")
    
    elif platform == "win32":
        print("Windows")
        os.chdir("D:\Coding\python\Dino\history")
    
    
    
    
    a = os.listdir()
    b = list(filter(lambda k: 'PVP' in k, a))
    
    
    for i in b:
        if os.path.isdir(i):
            print (i, end = '')
            print (' - ', end = '')
            os.chdir(i)
            t = os.listdir()       # list of CSV files in the directory - hopefully only 2
            b = list(filter(lambda k: '.csv' in k, t))
            
            t = os.getcwd().rfind("/")
            dataDate = os.getcwd()[t+1:t+11]
            
            plotBaseDir = "../" + dataDate + " "
            
            
            
            if (b[0].find("boost")>0):
                boostDataFile = b[0]
                dinoDataAllFile = b[1]
            else:
                boostDataFile = b[1]
                dinoDataAllFile = b[0]
                    
            boostData = pd.read_csv(rf'{boostDataFile}')
            boostData = boostData.rename(columns={'level': 'Level', 'cid':'Dino', 'attack boosts':'Attack', 'health boosts': 'Health', 'speed boosts':'Speed'})
            
            dinoDataAll = pd.read_csv(rf'{dinoDataAllFile}')
    
    
            if (tournamentID != 'PVP' ):
                dinoDataAll = dinoDataAll[dinoDataAll['dsid']==tournamentID]
            else:
                dinoDataAll = dinoDataAll[dinoDataAll['did']=="PVP"]
    
    
            if (dinoSelection == 'all'):
                dinoDataTop = dinoDataAll
                nTopBar = len(dinoDataAll)
            else:
                nTopBar = dinoSelection
                dinoDataTop = dinoDataAll[dinoDataAll['player_id']<nTopBar]
    
    
    ####### DATA UNPACKING 
    
            data = []
            
            for index, row in dinoDataTop.iterrows():
                currentTeam = literal_eval(row["cl"])
                currentPlayer = row ["player_id"]
                for j in range(len(currentTeam)) :
                    data.append([currentTeam[j],currentPlayer])
            
            
            #     print (currentTeam, currentPlayer)
            
            dinoTop = pd.DataFrame(data, columns=['Dino', 'player_id'])
            dinoTop.reset_index()
            dinoListTop= dinoTop["Dino"].unique()
            dinoListTop.sort()
    
    
            tournamentdinoDataAll = []
            tournamentDinoCount = []
            dinoCounter = 0; 
            for currentDino in dinoListTop:
                print(".", end = '')
                dinoCounter = dinoCounter +1 
                selectedDinos = boostData [boostData['Dino']==currentDino]
                selectedPlayers = dinoTop[dinoTop['Dino']==currentDino]
                sele = selectedPlayers["player_id"]
            
                tournamentDinoCount.append([currentDino, len(selectedPlayers), 100*len(selectedPlayers)/nTopBar])
            
                for currentPlayer in sele:
                    # dataframe
                    dinosauro = boostData[(boostData['Dino']==currentDino)&(boostData['player_id']==currentPlayer)]
                    # list
                    listaDino = dinosauro.values.tolist()
                    # flattened list
                    listaDino2 = list(chain.from_iterable(listaDino))
                    tournamentdinoDataAll.append(listaDino2)
            
    #        tournyDataTop = []
    #        tournyDinoTop = []
    #        tournyDataTop = pd.DataFrame(tournamentdinoDataAll, columns=list(boostData.columns))
    #        tournyDataTop.reset_index()
    #        tournyDataTop.to_csv(plotBaseDir+'tournyDataTop.csv')
    
    
    
            print (dinoCounter)
            
            tournyDinoTop = pd.DataFrame(tournamentDinoCount, columns=["Dino", "Count", "Count%"])
            tournyDinoTop = tournyDinoTop.sort_values(by=['Count%'], ascending=False)
            tournyDinoTop.reset_index()
            tournyDinoTop.to_csv(plotBaseDir+'tournyDinoTop ' + str(nTopBar) + '.csv')
                    
            
            
            os.chdir ('..') # last line of the for i in a loop
