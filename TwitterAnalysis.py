# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:24:51 2020

@author: Blake
"""

import pandas as pd
df = pd.read_csv(r'C:\Users\Blake\Desktop\TwitterScrapeResults.csv')
qb_list = ['Josh Allen','Cam Newton','Sam Darnold','Ryan Fitzpatrick','Derek Carr','Patrick Mahomes','Drew Lock','Justin Herbert','Ben Roethlisberger','Baker Mayfield','Joe Burrow','Lamar Jackson','Ryan Tannehill','Philip Rivers','Deshaun Watson','Gardner Minshew','Daniel Jones','Carson Wentz','Alex Smith','Andy Dalton','Aaron Rodgers','Nick Foles','Mitch Trubisky','Matthew Stafford','Kirk Cousins','Jared Goff','Kyler Murray','Russell Wilson','Jimmy Garoppolo','Tom Brady','Teddy Bridgewater','Matt Ryan','Drew Brees']
describe_list = ['sucks','great']
df['qb'].value_counts()
df['stringpassed']=df['qb'].str.cat(df['describe'],sep=" ")
summary = []
for x in qb_list:
    qb_sum = []
    name_of_qb = x
    qb_sum.append(name_of_qb)
    for j in describe_list:
        filt = df['stringpassed']== x+" "+j
        qb_sum.append(df.loc[filt]['stringpassed'].count())
    summary.append(qb_sum)

summarydf = pd.DataFrame(summary,columns=['Player','Sucks','Is Great'])
summarydf['HateIndex']=(summarydf['Sucks'])/((summarydf['Sucks'])+(summarydf['Is Great']))
qbrdf = pd.read_csv(r'C:\Users\Blake\Desktop\QBR.csv')
summarydf['QBR']=''
test = qbrdf[filt]['Value'].tolist()

summarydf = summarydf.set_index('Player')
qbrdf=qbrdf.set_index('Player')  
summarydf = summarydf.join(qbrdf,on = 'Player')  
summarydf=summarydf.reset_index()
from matplotlib import pyplot as plt
import seaborn as sns
ax = sns.regplot(summarydf['Value'],summarydf['HateIndex'],ci=None)
plt.xlabel('Passer Rating')
plt.ylabel('Hate Index')
plt.title('Comparing Quarterback Performance to Their Hate Index')
def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(point['x']+.02, point['y'], str(point['val']))
        
label_point(summarydf.Value, summarydf.HateIndex, summarydf.Player, plt.gca()) 
HateIndexDF = summarydf[['Player','HateIndex']].sort_values('HateIndex',ascending=False)
HateIndexDF= HateIndexDF.set_index('Player')