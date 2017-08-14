#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 14:55:57 2017

@author: anand
"""
#%%
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import *
sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
#testfile = sc.textFile("file:///home/anand/UvA/ING/Mechanical Turk/5/CPU50.csv")
ddf = sqlContext.read.format("com.databricks.spark.csv").option("header", "true").load("file:///home/anand/UvA/ING/Mechanical Turk/5/CPU50.csv")

#%%
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import Select, DatetimeTickFormatter, ColumnDataSource, BoxSelectTool, PolySelectTool, LassoSelectTool
from bokeh.layouts import widgetbox, row
from bokeh.events import Tap
import datetime
#%%
df = ddf.toPandas()#pd.read_csv("CPU50.csv",sep=",")
df['TIME'] = df['TIME'].apply(lambda x: x.split('.')[0])
df['TIMESTAMP'] = df['FK_DateKey'].astype(str) + " " + df['TIME'].astype(str)
df.iloc[:,-1] = pd.to_datetime(df.iloc[:,-1])
df['U_ID'] = df['JOB_NAME'].astype(str) + "_" + df['TIMESTAMP'].astype(str)
df['Annotate'] = np.zeros(df.shape[0]) 
df = df.sort_values(by=['TIMESTAMP'])
jobs = df.iloc[:,3].unique().tolist()

#%%
TOOLS="pan,wheel_zoom,reset,hover,poly_select,box_select,lasso_select"
def create_source(cpu):
    global rows    
    rows = np.where(df.iloc[:,3]==cpu)[0]
    data_dict = {'x':df.iloc[rows,-3], 'y':df.iloc[rows,-4]}
    return (ColumnDataSource(data=data_dict))


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def create_plot(source):    
    p = figure(tools=TOOLS,plot_width=960, plot_height=600)    
    p.circle('x','y',source=source,size=15, fill_color="firebrick", fill_alpha=0.3)   
    p.xaxis[0].formatter = DatetimeTickFormatter(days=['%m/%d', '%a%d']) 
    return p

def annotate(r_index):
    if isinstance(r_index,list):
        subset_arr = df.iloc[rows,-2].values
        for ind in r_index:            
            u_id = subset_arr[ind]
            print u_id
            loc = np.where(df.iloc[:,-2]==u_id)[0]
            print df.iloc[loc,-4]
            df.iloc[loc,-1] = 1
        df.to_csv("annotated.csv", sep = ',', index=False, encoding = 'utf8')
            
    else:
        u_id = df.iloc[rows,-2][r_index]
        print u_id
        loc = np.where(df.iloc[:,-2]==u_id)[0]
        print loc
        df.iloc[loc,-1] = 1
        df.to_csv("annotated.csv", sep = ',', index=False, encoding = 'utf8')
        
        
    
    
#%%
def function_to_call(attr, old, new):    
    cpu_job = select.value    
    src = create_source(cpu_job)
    source.data.update(src.data)
    print cpu_job    
    
    
def onclick_event(event):
    print('Python:Click')
    print (event.x)
    print (event.y)
    xclick = datetime.datetime.fromtimestamp(event.x/1e3)
    r_index = find_nearest(df.iloc[rows,-3],xclick)
    print len(df.iloc[rows,-3])
    print r_index
    annotate(r_index)
    
    
def callback(attr, old, new):
    r_indices = source.selected['1d']['indices']
    annotate(r_indices)
    
#%% main
cpu_job = jobs[0]
select = Select(options=jobs, value=cpu_job, title="CPU_Jobs")

source = create_source(cpu_job)
source.on_change('selected',callback)

plot = create_plot(source)
select.on_change('value', function_to_call)

#select_tool = plot.select(dict(type=BoxSelectTool))[0]

layout = row(plot,widgetbox(select))
#layout.children[0].on_event(Tap,onclick_event)

curdoc().add_root(layout)



