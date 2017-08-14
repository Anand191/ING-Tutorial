#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 10:43:36 2017

@author: anand
"""

#%%
from pyspark import SparkContext
from pyspark.sql import SQLContext
#from pyspark.sql.types import *
from os import path

basedir = "/home/anand/UvA/ING/Mechanical Turk/5"

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

ddf = sqlContext.read.format("com.databricks.spark.csv").option("header", "true").load(path.join(basedir,"CPU50.csv"))

#%%
import pandas as pd
import numpy as np
from pandas.plotting import autocorrelation_plot, lag_plot
import matplotlib.pyplot as plt

#%%
df = pd.read_csv(path.join(basedir,"CPU50.csv"),sep=",")
df['TIME'] = df['TIME'].apply(lambda x: x.split('.')[0])
df['TIMESTAMP'] = df['FK_DateKey'].astype(str) + " " + df['TIME'].astype(str)
df.iloc[:,-1] = pd.to_datetime(df.iloc[:,-1])
df['U_ID'] = df['JOB_NAME'].astype(str) + "_" + df['TIMESTAMP'].astype(str)
df['Annotate'] = np.zeros(df.shape[0]) 
df = df.sort_values(by=['TIMESTAMP'])
jobs = df.iloc[:,3].unique().tolist()
#%%
plt.figure(figsize=(18,14))
rows = np.where(df.iloc[:,3]==jobs[19])[0]
autocorrelation_plot(df.iloc[rows,-4])
#lag_plot(df.iloc[rows,-4])
plt.show()
