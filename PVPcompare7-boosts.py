'''
2022-05-29

@author: DeepShadow


PLOTS THE BOOST DISTRIBUTIONS FOR TWO SET OF DATA (top 50 and remaining top250, for example)

This should work automatically once the correct filenames are added to boostDataFile and dinoDataAllFile,
and the correct tournamentID/PVP ID is used for tournamentID

To be used when all player IDs are ordered

Folder names in lines 90/94 should be adjusted to match the machine currently used


'''


''' TODO 

- set the threshold on the total counter, not the partial ones

'''



#### THESE NEED TO BE CHANGED ####
tournamentName = "2022-11-11 advantage rare common"
boostDataFile = 'Champ_CR_All_Adv_Ankylosa2_Alanqa-dino_boosts.csv'
dinoDataAllFile = 'Champ_CR_All_Adv_Ankylosa2_AlanqaCPG_HXOCUQ71KBML3HRR-Q4G5G50049TF3JS2-EVT_LVGLA2PL0QLLMHA6200-dino_teams.csv'
# dinoDataTopFile = '2022-05_Season_-_Ailurarctos 500-dino_teams.csv'

# for PVP team, use tournamentID = 'PVP'
# tournamentID = 'PVP'
tournamentID = "CPG_HXOCUQ71KBML3HRR-Q4G5G50049TF3JS2-EVT_LVGLA2PL0QLLMHA6"
tournamentID = tournamentID.replace("-", "/")
# NEXT STEP: automatic extraction from dinoDataAllFile

# minimum number of dinos to visualise
# - below this threshold there are just too few data for a nice graph
nThreshold = 5
nTopBar = 50


###### THE REST SHOULD WORK AUTOMATICALLY


plotBaseDir = './'+tournamentName+'/'    # remember the final /
tournament_string = tournamentName + " "


import warnings
warnings.filterwarnings("ignore")
# import io
import pandas as pd
import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns

import os

from ast import literal_eval
from itertools import chain


from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H.%M.%S ")




#from js import fetch
#import json

# res = await fetch('https://jupyterlite.anaconda.cloud/b0df9a1c-3954-4c78-96e6-07ab473bea1a/files/bikeshare.csv')
# csv_data = await res.text()

# df = pd.read_csv(io.StringIO(csv_data))
# df.head()



    if platform == "darwin":
        print('Mac OS X')
        os.chdir("/Users/Coding/python/Dino/history")
    
    elif platform == "win32":
        print("Windows")
        os.chdir("D:\Coding\python\Dino\history")
 


'''
####################################################################################
'''


print('Data reading')


boostData = pd.read_csv(rf'{plotBaseDir}{boostDataFile}')
# dinoDataTop = pd.read_csv(rf'{plotBaseDir}{dinoDataTopFile}')
dinoDataAll = pd.read_csv(rf'{plotBaseDir}{dinoDataAllFile}')

dinoDataTop = dinoDataAll[dinoDataAll['player_id']<nTopBar]
#dinoDataAll = dinoDataAll[dinoDataAll['player_id']<2]



boostData = boostData.rename(columns={'level': 'Level', 'cid':'Dino', 'attack boosts':'Attack', 'health boosts': 'Health', 'speed boosts':'Speed'})

# four tournaments, set the tournamentID then select the data based on 'dsid"
# tournamentID = 'CPG_0EO7SF4HOK4N9I67/SPWAW5YJMWJYAXP7/EVT_LVGLA2PL0QLLMHA6'

if (tournamentID != 'PVP' ):
    dinoDataAll = dinoDataAll[dinoDataAll['dsid']==tournamentID]
    dinoDataTop = dinoDataTop[dinoDataTop['dsid']==tournamentID]
else:
    dinoDataAll = dinoDataAll[dinoDataAll['did']=="PVP"]
    dinoDataTop = dinoDataTop[dinoDataTop['did']=="PVP"]


# THIS COMMAND IS NEEDED IF THE "ALL" LIST CONTAINST THE TOP AS WELL
# IT REMOVES THE TOP TEAMS FROM THE ALL ONE
dinoDataRest = pd.merge(dinoDataAll, dinoDataTop, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)


# not really sure if these mean anything at all...
boostData.reset_index()
dinoDataRest.reset_index()
dinoDataTop.reset_index()


#### THESE COULD BE CHANGED ####

# VARIOUS PARAMETERS FOR THE PLOTS
fAlpha = 0.5
vpBandwidth = 0.15;
tickLabelsBoosts = np.linspace (1,20,20)
tickLabelsLevels = np.linspace (1,30,30)
violin_plot_width =  1.3 # (dino_scale + float(dino_numbers['Count%']))/(100+dino_scale)

sns.set_theme(style="whitegrid")
# sns.set_theme(style="darkgrid")


# LET THE GAME BEGIN

'''
####################################################################################
'''
print('Data processing')


# STEP 1: unpack the dinos used in the teams


data = []

for index, row in dinoDataRest.iterrows():
    currentTeam = literal_eval(row["cl"])
    currentPlayer = row ["player_id"]
    for j in range(len(currentTeam)) :
        data.append([currentTeam[j],currentPlayer])


#     print (currentTeam, currentPlayer)

dinoAll = pd.DataFrame(data, columns=['Dino', 'player_id'])
dinoAll.reset_index()
dinoListAll = dinoAll["Dino"].unique()
dinoListAll.sort()

# dinoTop contains the 150*8 dinos used by the top 150 players
# dinoList contains their names



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

nNumberOfPlayersAll = len(dinoDataRest)
nNumberOfPlayersTop = len(dinoDataTop)




tournamentdinoDataAll = []
tournamentDinoCount = []
for currentDino in dinoListTop:
    selectedDinos = boostData [boostData['Dino']==currentDino]
    selectedPlayers = dinoTop[dinoTop['Dino']==currentDino]
    sele = selectedPlayers["player_id"]

    tournamentDinoCount.append([currentDino, len(selectedPlayers), 100*len(selectedPlayers)/nNumberOfPlayersTop])

    for currentPlayer in sele:
        # dataframe
        dinosauro = boostData[(boostData['Dino']==currentDino)&(boostData['player_id']==currentPlayer)]
        # list
        listaDino = dinosauro.values.tolist()
        # flattened list
        listaDino2 = list(chain.from_iterable(listaDino))
        tournamentdinoDataAll.append(listaDino2)

tournyDataTop = []
tournyDinoTop = []
tournyDataTop = pd.DataFrame(tournamentdinoDataAll, columns=list(boostData.columns))
tournyDataTop.reset_index()
tournyDataTop.to_csv(plotBaseDir+'tournyDataTop.csv',index=False)

tournyDinoTop = pd.DataFrame(tournamentDinoCount, columns=["Dino", "Count", "Count%"])
tournyDinoTop = tournyDinoTop.sort_values(by=['Count'], ascending=False)
tournyDinoTop.reset_index()
tournyDinoTop.to_csv(plotBaseDir+'tournyDinoTop.csv',index=False)




tournamentdinoDataAll = []
tournamentDinoCount = []

for currentDino in dinoListAll:
    selectedDinos = boostData [boostData['Dino']==currentDino]
    selectedPlayers = dinoAll[dinoAll['Dino']==currentDino]
    sele = selectedPlayers["player_id"]

    thisIsNow = [currentDino, len(selectedPlayers), 100*len(selectedPlayers)/nNumberOfPlayersAll]
    tournamentDinoCount.append(thisIsNow)


    for currentPlayer in sele:
        # dataframe
        dinosauro = boostData[(boostData['Dino']==currentDino)&(boostData['player_id']==currentPlayer)]
        # list
        listaDino = dinosauro.values.tolist()
        # flattened list
        listaDino2 = list(chain.from_iterable(listaDino))
        tournamentdinoDataAll.append(listaDino2)

tournyDataAll = []
tournyDinoAll = []
tournyDataAll = pd.DataFrame(tournamentdinoDataAll, columns=list(boostData.columns))
tournyDataAll.reset_index()
tournyDataAll.to_csv(plotBaseDir+'tournyDataAll.csv',index=False)

tournyDinoAll = pd.DataFrame(tournamentDinoCount, columns=["Dino", "Count", "Count%"])
tournyDinoAll = tournyDinoAll.sort_values(by=['Count'], ascending=False)
tournyDinoAll.reset_index()
tournyDinoAll.to_csv(plotBaseDir+'tournyDinoAll.csv',index=False)



'''
####################################################################################
'''
# STEP 2: plot the dino stats
print('Plotting')
TopString = 'Players 1-' + str(nNumberOfPlayersTop)
BottomString = 'Players ' + str(nNumberOfPlayersTop+1) + '-' + str(nNumberOfPlayersTop+nNumberOfPlayersAll)



# for currentDino in dinoList:

for index, row in tournyDinoTop.iterrows():

    currentDino = row['Dino']


    currentdinoDataAll = tournyDataAll[tournyDataAll['Dino']==currentDino]
    currentdinoDataTop = tournyDataTop[tournyDataTop['Dino']==currentDino]

    nDtop = len(currentdinoDataTop)
    nDall = len(currentdinoDataAll)


    # THIS MIGHT BE NEEDED 
    plt.rcParams['figure.dpi'] = 300

    if (np.logical_or (nDtop>nThreshold, nDall>nThreshold)):
        print (currentDino)

        filename = plotBaseDir + 'cmp - ' + currentDino+  ".png"


#TODO CHECK SCREEN RESOLUTION
# px = 1/plt.rcParams['figure.dpi']  # pixel in inches
# plt.subplots(figsize=(600*px, 200*px))


        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6), gridspec_kw={'width_ratios': [1,1,3]})
#        figureTitle = dt_string + " - " + currentDino + ": " + str(row['Count']) + " - " + '{:.1f}'.format(row['Count%']) +"%"

#        figureTitle = dt_string + " - " + currentDino + ": " + str(nDtop) + "/" + str(nNumberOfPlayersTop)
        figureTitle = tournament_string + " - " + currentDino + ": " + str(nDtop) + "/" + str(nNumberOfPlayersTop)




        figureTitle = figureTitle + " - " + str(nDall) + "/" + str(nNumberOfPlayersAll)

        fig.suptitle(figureTitle)


        currentdinoDataAll['rank'] = BottomString
        currentdinoDataTop['rank'] =    TopString

        data = pd.concat( [currentdinoDataAll, currentdinoDataTop])
        data.reset_index()

        data['Health'] = data['Health']/100
        data['Attack'] = data['Attack']/100
        data['Speed'] = data['Speed']/100
        
        data['Boosts'] = data['Health']+data['Attack']+data['Speed']

        # 'variable', 'value' and 'rank' come from these melts
        data1 = pd.melt(data, value_vars=[ 'Level'], id_vars='rank')
        data2 = pd.melt(data, value_vars=[ 'Boosts'], id_vars='rank')
        data3 = pd.melt(data, value_vars=[ 'Health', 'Attack', 'Speed'] , id_vars='rank')



# DINO LEVEL

        dino_plot = sns.violinplot( x='variable', y='value', hue='rank',
                       data=data1,
                       split=True,
                       inner="quartile",
                       linewidth=1.5,
                       width=violin_plot_width,
                       palette="Accent", #{TopString: "b", BottomString: "r"} ,
                       hue_order= [TopString, BottomString],
                       scale="area",
                       cut=0,
                       bw= vpBandwidth,
                       ax = ax1)

        for l in dino_plot.lines:
            l.set_linestyle('--')
            l.set_linewidth(1.5)
            l.set_color('red')
            l.set_alpha(0.8)
        for l in dino_plot.lines[1::3]:
            l.set_linestyle('-')
            l.set_linewidth(3)
            l.set_color('black')
            l.set_alpha(0.8)




        ax1.set_ylim(0, 30)
        leg = ax1.legend(loc='lower center') #,labels=["1-249","249-459"])
#        for lh in leg.legendHandles:
#            lh.set_alpha(fAlpha)

        ax1.set_ylabel('Dinosaur level')
        ax1.set_xlabel('')
        ax1.set_yticks (tickLabelsLevels)
        plt.setp(ax1.collections, alpha=fAlpha)

# BOOST LEVEL

        dino_plot = sns.violinplot( x='variable', y='value', hue='rank',
                       data=data2,
                       split=True,
                       inner="quartile",
                       linewidth=1.5,
                       width=violin_plot_width,
                       palette="Accent", #{TopString: "b", BottomString: "r"} ,
                       hue_order= [TopString, BottomString],
                       scale="area",
                       cut=0,
                       bw= vpBandwidth,
                       ax = ax2)

        for l in dino_plot.lines:
            l.set_linestyle('--')
            l.set_linewidth(1.5)
            l.set_color('red')
            l.set_alpha(0.8)
        for l in dino_plot.lines[1::3]:
            l.set_linestyle('-')
            l.set_linewidth(3)
            l.set_color('black')
            l.set_alpha(0.8)


        ax2.set_ylim(0, 30)
        ax2.get_legend().remove()
        ax2.set_ylabel('Total number of applied boosts')
        ax2.set_xlabel('')
        ax2.set_yticks (tickLabelsLevels)
        plt.setp(ax2.collections, alpha=fAlpha)



# BOOSTS DISTRIBUTION

        dino_plot = sns.violinplot( x='variable', y='value',  hue='rank',
                       data=data3,
                       split=True,
                       inner="quartile",
                       linewidth=1.5,
                       width=violin_plot_width,
                       palette="Accent", #{TopString: "b", BottomString: "r"},
                       hue_order= [TopString, BottomString],
                       scale="area",
                       cut=0,
                       bw= vpBandwidth,
                       ax = ax3)

        for l in dino_plot.lines:
            l.set_linestyle('--')
            l.set_linewidth(1.5)
            l.set_color('red')
            l.set_alpha(0.8)
        for l in dino_plot.lines[1::3]:
            l.set_linestyle('-.')
            l.set_linewidth(3)
            l.set_color('black')
            l.set_alpha(0.8)

        ax3.set_ylim(0, 20)
        ax3.get_legend().remove()
        ax3.set_ylabel('Boost levels')
        ax3.set_xlabel('')
        ax3.set_yticks (tickLabelsBoosts)
        plt.setp(ax3.collections, alpha=fAlpha)


        sns.despine()
        fig.tight_layout()

        fig = dino_plot.get_figure()
        fig.savefig(filename)



#palette="Set2"
#palette={"Top": "b", "Bottom": "r"}





#        dino_numbers = DCtop [DCtop['Dino']==currentDino]
#        dino_scale = 30
