#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:00:16 2017

@author: anand
"""
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from os import path
import sklearn as sk
from sklearn.cluster import KMeans
import os

#%%
basedir = path.join(os.pardir,"Data")
df = pd.read_excel(path.join(basedir,'sat.xlsx'), header=None)

#%%
X = df.iloc[0:3500,0:36]
kmeans = KMeans(n_clusters=3,random_state=0).fit(X)
#print (kmeans.labels_)
Y = kmeans.predict(df.iloc[3500:4435,0:36])
#print (kmeans.cluster_centers_)
