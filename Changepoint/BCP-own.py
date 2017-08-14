#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import division
"""
Created on Fri Aug  4 11:17:19 2017

@author: anand
"""

#%%
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pandas as pd
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
jobs = df.iloc[:,3].unique().tolist()

rows = np.where(df.iloc[:,3]==jobs[10])[0]
xcoord = df.iloc[rows,-3]
data = df.iloc[rows,-4]


fig, ax = plt.subplots(figsize=[16, 12])
ax.plot(xcoord,data)

#%%
# =============================================================================
# import cProfile
# import bayesian_changepoint_detection.offline_changepoint_detection as offcd
# from functools import partial
# 
# Q, P, Pcp = offcd.offline_changepoint_detection(data, partial(offcd.const_prior, l=(len(data)+1)), 
#                                                 offcd.gaussian_obs_log_likelihood, truncate=-40)
# 
# 
# fig, ax = plt.subplots(figsize=[18, 16])
# ax = fig.add_subplot(2, 1, 1)
# ax.plot(data[:])
# ax = fig.add_subplot(2, 1, 2, sharex=ax)
# ax.plot(np.exp(Pcp).sum(0))
# =============================================================================

#%%

import bayesian_changepoint_detection.online_changepoint_detection as oncd
from functools import partial
import matplotlib.cm as cm

R, maxes = oncd.online_changepoint_detection(data, partial(oncd.constant_hazard, 250), oncd.StudentT(0.1, .01, 1, 0))


fig, ax = plt.subplots(figsize=[18, 16])
ax = fig.add_subplot(3, 1, 1)
ax.plot(xcoord,data)
ax = fig.add_subplot(3, 1, 2, sharex=ax)
sparsity = 5  # only plot every fifth data for faster display
ax.pcolor(np.array(range(0, len(R[:,0]), sparsity)), 
          np.array(range(0, len(R[:,0]), sparsity)), 
          -np.log(R[0:-1:sparsity, 0:-1:sparsity]), 
          cmap=cm.Greys, vmin=0, vmax=30)
ax = fig.add_subplot(3, 1, 3, sharex=ax)
Nw=10;
ax.plot(R[Nw,Nw:-1])