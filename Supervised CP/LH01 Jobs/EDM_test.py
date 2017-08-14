#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 14:58:43 2017

@author: anand
"""

import breakout_detection
import pandas_datareader.data as web 
import matplotlib.pyplot as plt 

plt.style.use('fivethirtyeight')
edm_multi = breakout_detection.EdmMulti() 
snp = web.DataReader('^GSPC', 'yahoo') 
max_snp = max(max(snp['Open']),1) 
Z = [x/float(max_snp) for x in snp['Open']]
#args format = ['min_size (int)', 'beta (float)', 'degree (int)']
args = [64, 0.0001, 1]
edm_multi.evaluate(Z,*args)

#Note evaluate in EdmMulti has been defined with *args, and therefore should only accepts values
#of the arguments min_size/beta/degree in that order (type: int/float/int). In order to provide named arguments 
#viz. min_size=64, beta =0.0001,degree=1 we need to define EdmMulti with **kwargs

snp['Open'].plot(figsize=(12,10)) 
for i in edm_multi.getLoc(): 
    plt.axvline(snp['Open'].index[i], color='#FF4E24')