#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 14:38:55 2017

@author: anand
"""
#%%
import pandas as pd
import numpy as np
from changepy.costs import normal_meanvar
from changepy import pelt
from changepoint.mean_shift_model import MeanShiftModel
import matplotlib.pyplot as plt

#%%
df = pd.read_csv("CPU50.csv",sep=",")
df['TIME'] = df['TIME'].apply(lambda x: x.split('.')[0])
df['TIMESTAMP'] = df['FK_DateKey'].astype(str) + " " + df['TIME'].astype(str)
df.iloc[:,-1] = pd.to_datetime(df.iloc[:,-1])
df['U_ID'] = df['JOB_NAME'].astype(str) + "_" + df['TIMESTAMP'].astype(str)
df['Annotate'] = np.zeros(df.shape[0]) 
df = df.sort_values(by=['TIMESTAMP'])
#df.to_csv('chk.csv',sep=',',encoding='utf8')
jobs = df.iloc[:,3].unique().tolist()

#%%
np.random.shuffle(jobs)
fig = plt.figure(figsize=(12,10))
z = 1
N = int(np.sqrt(9))

model = MeanShiftModel()
for i in xrange(N**2):
    cpu = jobs[i]
    rows = np.where(df.iloc[:,3]==cpu)[0]
    xaxis = df.iloc[rows,-3].values
    ts = df.iloc[rows,-4]
    breakouts = pelt(normal_meanvar(ts),len(ts))
    plt.subplot(N,N,z)
    #ts.plot(kind='hist')
    #z+= 1
    plt.plot(xaxis,df.iloc[rows,-4])
    #plt.axvline(xaxis[breakouts[1000]],color='red',linestyle='--')
    for xc in breakouts:
        plt.axvline(x=xaxis[xc],color='red',linestyle='--')
    z += 1
    