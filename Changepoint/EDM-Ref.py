#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 15:26:36 2017

@author: anand
"""

import pandas as pd 
import breakout_detection 
import pandas_datareader.data as web 
import matplotlib.pyplot as plt 

plt.style.use('fivethirtyeight')
edm_multi = breakout_detection.EdmMulti() 
snp = web.DataReader('^GSPC', 'yahoo') 
max_snp = max(max(snp['Open']),1) 
Z = [x/float(max_snp) for x in snp['Open']] 
edm_multi.evaluate(Z,min_size = 64) 
snp['Open'].plot(figsize=(30,10)) 
for i in edm_multi.getLoc(): 
    plt.axvline(snp['Open'].index[i], color='#FF4E24')
                
                
