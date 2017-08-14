#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:37:05 2017

@author: anand
"""
#%%
import pandas as pd
import breakout_detection as bd
import matplotlib.pyplot as plt
import numpy as np
import os

#%%
dir2 = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(dir2,'CPU50.csv'),sep=",")
df['TIME'] = df['TIME'].apply(lambda x: x.split('.')[0])
df['TIMESTAMP'] = df['FK_DateKey'].astype(str) + " " + df['TIME'].astype(str)
df.iloc[:,-1] = pd.to_datetime(df.iloc[:,-1])
df['U_ID'] = df['JOB_NAME'].astype(str) + "_" + df['TIMESTAMP'].astype(str)
df['Annotate'] = np.zeros(df.shape[0]) 
df = df.sort_values(by=['TIMESTAMP'])
#df.to_csv('chk.csv',sep=',',encoding='utf8')
jobs = df['JOB_NAME'].unique().tolist()

rows = np.where(df['JOB_NAME']=="WLM")[0]
xcoord = df['TIMESTAMP'].iloc[rows]
data = df['MSU_CPU'].iloc[rows]

xcoord = xcoord.tolist()
data = data.tolist()


# =============================================================================
# fig, ax = plt.subplots(figsize=[16, 12])
# ax.plot(xcoord,data)
# =============================================================================

#%%
edm = bd.EdmMulti()
edm.evaluate(data)
fig, ax = plt.subplots(figsize=[12, 10])
ax.plot(xcoord,data)
loc = edm.getLoc()
for i in loc: 
    ax.axvline(xcoord[i], color='#FF4E24', ls='dotted',lw=1.0)
               

edm.evaluate.im_func
