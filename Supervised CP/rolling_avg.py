#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 11:20:59 2017

@author: anand
"""
#%%
import pandas as pd
import numpy as np
from datetime import datetime
import os
import matplotlib.pyplot as plt


#%%
dir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(dir,'CPU50.csv'),sep=",")
df['TIME'] = df['TIME'].apply(lambda x: x.split('.')[0])
df['TIMESTAMP'] = df['FK_DateKey'].astype(str) + " " + df['TIME'].astype(str)
df.iloc[:,-1] = pd.to_datetime(df.iloc[:,-1])
df['U_ID'] = df['JOB_NAME'].astype(str) + "_" + df['TIMESTAMP'].astype(str)
df['Z_Score'] = np.zeros(df.shape[0])
df['Scaled'] = np.zeros(df.shape[0])
df['Rolling'] = np.zeros(df.shape[0])
df['Annotate'] = np.zeros(df.shape[0])
df = df.sort_values(by=['TIMESTAMP'])

jobs = df['JOB_NAME'].unique().tolist()

for job in jobs:
    r = np.where(df['JOB_NAME']==job)[0]
    mean = df['MSU_CPU'].iloc[r].mean()
    std = df['MSU_CPU'].iloc[r].std()
    min_d = df['MSU_CPU'].iloc[r].min()
    max_d = df['MSU_CPU'].iloc[r].max()
    
    df['Z_Score'].iloc[r] = (df['MSU_CPU'] - mean)/std
    df['Scaled'].iloc[r] = (df['MSU_CPU'].iloc[r] - min_d)/(max_d - min_d)
    
    rolling = df['MSU_CPU'].iloc[r].rolling(window=4)
    df['Rolling'].iloc[r] = rolling.mean()    
    rows = np.where(np.isnan(df['Rolling']))[0]
    df['Rolling'].iloc[rows] = df['MSU_CPU'].iloc[rows]
    
    
#%%
row = np.where(df['JOB_NAME']=='CTD001AH')[0]
plt.plot(df['Rolling'].iloc[row],color='r',marker='o')
df['MSU_CPU'].iloc[row].plot(color='b')
    