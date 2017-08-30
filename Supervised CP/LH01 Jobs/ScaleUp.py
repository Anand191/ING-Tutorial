#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:43:37 2017

@author: anand
"""

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
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import os
import breakout_detection
#import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from rpy2.robjects.packages import importr
import rpy2.robjects.numpy2ri
import time

#testfile = sc.textFile("file:///home/anand/UvA/ING/Mechanical Turk/5/CPU50.csv")
    
def scaled_up(ssq):    
    df = sqlContext.read.format("com.databricks.spark.csv").option("header", "true").load("file:///{}".format(master_file))
    df = df.withColumn('JOB_NAME',df['JOB_NAME'].cast('string') )
    df = df.withColumn('Annotate',df['Annotate'].cast('integer') )
    df = df.withColumn('MSU_CPU',df['MSU_CPU'].cast('float') )
    df = df.withColumn('Z_Score',df['Z_Score'].cast('float') )
    df = df.withColumn('Scaled',df['Scaled'].cast('float') )
    df = df.withColumn('Rolling_Mean',df['Rolling_Mean'].cast('float') )
    df = df.withColumn('Rolling_Median',df['Rolling_Median'].cast('float') )
    
    #%%
  
    
    #%%
    base = importr('base')
    utils = importr('utils')
    ecp = importr('ecp')
    cp = importr('changepoint')
    
    #%%
    col1 = np.array(df.select('JOB_NAME').collect())
    #col1 = col1.astype(str)
    col2 = np.array(df.select('MSU_CPU').collect())
    col3 = np.array(df.select('Z_Score').collect())
    col4 = np.array(df.select('Scaled').collect())
    col5 = np.array(df.select('Rolling_Mean').collect())
    col6 = np.array(df.select('Rolling_Median').collect())
    X = np.column_stack((col1,col2,col3,col4,col5,col6))
    Y= np.array(df.select('Rolling_Median').collect())
    jobs = np.unique(X[:,0])
    edm_multi = breakout_detection.EdmMulti()
    
    
    #%%
    
    for job in jobs:
        rows = np.where(X[:,0]==job)[0]
        data = X[rows,1:]
        xcoord = np.arange(len(data))
        label = Y[rows]
        
        ddf = df.filter(df['JOB_NAME'] == job).groupby('FK_DateKey').agg({'TIME':'count'})
        min_size = int(ddf.agg({'count(TIME)':'mean'}).collect()[0][0])*5
        beta = 0.0001
        degree = 1
        args = [min_size,beta,degree]    
        edm_multi.evaluate(X[rows,1].astype(float),*args)   
        
        
        plt.figure(figsize=(12,8))
        plt.subplot(1,1,1)
        plt.plot(xcoord,data[:,-1])
        loc = edm_multi.getLoc()                   
        for j in loc:
            plt.axvline(j,color='g',ls='dashed',lw="1.0")
        #plt.show()
#%%
if __name__ == '__main__':  
    rpy2.robjects.numpy2ri.activate()
    dir2 = os.path.dirname(__file__)
    master_file = os.path.join(dir2,'annotated.csv')
    sc = SparkContext.getOrCreate()
    sqlContext = SQLContext(sc)
    start = time.time()
    scaled_up(sqlContext)
    end = time.time()
    print(end - start)
 
