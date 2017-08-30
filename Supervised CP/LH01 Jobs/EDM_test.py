#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:58:43 2017

@author: anand


Note evaluate in EdmMulti has been defined with *args, and therefore should only accepts values
of the arguments min_size/beta/degree in that order (type: int/float/int). In order to provide named arguments 
viz. min_size=64, beta =0.0001,degree=1 we need to define EdmMulti with **kwargs
"""
#%%
import breakout_detection
import pandas_datareader.data as web
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%
df = pd.read_csv('annotated.csv', sep = ',')
df['Annotate'] = df['Annotate'].astype(int)

#%%
X = np.column_stack((df['JOB_NAME'],df['MSU_CPU'],df['Z_Score'],df['Scaled'],df['Rolling_Mean'],df['Rolling_Median']))
Y= df.iloc[:,-2].values
jobs = np.unique(X[:,0])
edm_multi = breakout_detection.EdmMulti()


#%%

for job in jobs:
    rows = np.where(X[:,0]==job)[0]
    data = X[rows,1:]
    xcoord = np.arange(len(data))
    label = Y[rows]
    
    min_size = int(df.iloc[rows,:].groupby('FK_DateKey')['TIME'].count().mean())*5
    beta = 0.0001
    degree = 1
    args = [min_size,beta,degree]    
    edm_multi.evaluate(X[rows,1],*args)
    
    plt.figure(figsize=(12,8))
    plt.plot(xcoord,data[:,-1])
    
# =============================================================================
#     count = 0
#     for i in xrange(len(label)-1):
#         if (label[i] != label[i+1]):
#             count += 1
#             plt.axvline(i, color='#FF4E24',lw=1.0)
# =============================================================================
                        
    loc = edm_multi.getLoc()                   
    for j in edm_multi.getLoc():
        plt.axvline(j,color='g',ls='dashed',lw="1.0")
 
#%%Test Case
# =============================================================================
# plt.style.use('fivethirtyeight')
# edm_multi = breakout_detection.EdmMulti() 
# snp = web.DataReader('^GSPC', 'yahoo') 
# max_snp = max(max(snp['Open']),1) 
# Z = [x/float(max_snp) for x in snp['Open']]
# #args format = ['min_size (int)', 'beta (float)', 'degree (int)']
# args = [64,0.0001,1]
# edm_multi.evaluate(Z,*args)
# 
# 
# 
# snp['Open'].plot(figsize=(12,10)) 
# for i in edm_multi.getLoc(): 
#     plt.axvline(snp['Open'].index[i], color='#FF4E24')
# 
# =============================================================================
