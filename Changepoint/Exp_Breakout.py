#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 15:02:48 2017

@author: anand
"""

import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import pandas as pd
import numpy as np
from rpy2.robjects.vectors import StrVector

#%%
base = importr('base')
utils = importr('utils')

devtools = importr('devtools')
#breakout = importr('BreakoutDetection')

#%%
df = pd.read_csv("CPU50.csv",sep=",")
df['TIME'] = df['TIME'].apply(lambda x: x.split('.')[0])
df['TIMESTAMP'] = df['FK_DateKey'].astype(str) + " " + df['TIME'].astype(str)
df.iloc[:,-1] = pd.to_datetime(df.iloc[:,-1])
df['U_ID'] = df['JOB_NAME'].astype(str) + "_" + df['TIMESTAMP'].astype(str)
df['Annotate'] = np.zeros(df.shape[0]) 
df = df.sort_values(by=['TIMESTAMP'])


