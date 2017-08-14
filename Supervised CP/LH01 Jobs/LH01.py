#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 15:49:38 2017

@author: anand
"""

import pandas as pd

df = pd.read_csv("LH012017.csv",sep=";",header=None)
df2 = pd.DataFrame(df.values,columns=['FK_DateKey','TIME','MVS_SYSTEM_ID','JOB_NAME','MSU_CPU'])
df2['MSU_CPU'] = df2['MSU_CPU'].apply(lambda x: x.replace(',','.'))
df2['MSU_CPU'] = pd.to_numeric(df2['MSU_CPU'])
#%%
df2.to_csv("LH01.csv",sep=",", index=None)