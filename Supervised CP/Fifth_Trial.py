#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 14:55:57 2017

@author: anand
"""
#%%
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models import Select, DatetimeTickFormatter, ColumnDataSource, BoxSelectTool,LassoSelectTool
from bokeh.layouts import widgetbox, row
from bokeh.events import Tap
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
#%%
#dir1 = os.path.dirname(os.path.dirname(__file__))
dir2 = os.path.dirname(__file__)
db_file = os.path.join(dir2,'cdb.db')

engine = create_engine('sqlite:///{}'.format(db_file),echo=False)
Base = declarative_base(engine)

meta = MetaData(engine)
db = Table('cdb1', meta, autoload=True)
    
Session = sessionmaker(bind=engine)
session = Session()

#%%

# =============================================================================
# df = pd.read_csv(os.path.join(dir2,'CPU50.csv'),sep=",")
# df['TIME'] = df['TIME'].apply(lambda x: x.split('.')[0])
# df['TIMESTAMP'] = df['FK_DateKey'].astype(str) + " " + df['TIME'].astype(str)
# df.iloc[:,-1] = pd.to_datetime(df.iloc[:,-1])
# df['U_ID'] = df['JOB_NAME'].astype(str) + "_" + df['TIMESTAMP'].astype(str)
# df['Z-Score'] = np.zeros(df.shape[0])
# df['Scaled'] = np.zeros(df.shape[0])
# df['Annotate'] = np.zeros(df.shape[0])
# df = df.sort_values(by=['TIMESTAMP'])
# =============================================================================
df = pd.read_sql_table('cdb1',con=engine)

jobs = df['JOB_NAME'].unique().tolist()

# =============================================================================
# for job in jobs:
#     r = np.where(df['JOB_NAME']==job)[0]
#     mean = df['MSU_CPU'].iloc[r].mean()
#     std = df['MSU_CPU'].iloc[r].std()
#     min_d = df['MSU_CPU'].iloc[r].min()
#     max_d = df['MSU_CPU'].iloc[r].max()
#     df['Scaled'].iloc[r] = (df['MSU_CPU'].iloc[r] - min_d)/(max_d - min_d)
# =============================================================================





#%%
TOOLS="pan,wheel_zoom,reset,hover,box_select,lasso_select"
def create_source(cpu):
    global rows    
    rows = np.where(df['JOB_NAME']==cpu)[0]
    data_dict = {'x':df['TIMESTAMP'].iloc[rows], 'y':df['Rolling'].iloc[rows]}
    return (ColumnDataSource(data=data_dict))


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    return idx

def create_plot(source):    
    p = figure(tools=TOOLS,plot_width=960, plot_height=600)    #output_backend="webgl"
    p.circle('x','y',source=source,size=8, fill_color="firebrick", fill_alpha=0.3)
    p.line('x','y',source=source,line_width=1,line_dash='dashed',line_alpha=0.5)
    p.xaxis[0].formatter = DatetimeTickFormatter(days=['%m/%d', '%a%d']) 
    return p

def annotate(r_index):
    ddf = df
    if isinstance(r_index,list):
        subset_arr = ddf['U_ID'].iloc[rows].values
        for ind in r_index:            
            u_id = subset_arr[ind]
            print (u_id)
            loc = np.where(ddf['U_ID']==u_id)[0]
            print (ddf['MSU_CPU'].iloc[loc])
            #ddf.iloc[loc,-1] = 1
            u = update(db).where(db.c.U_ID == u_id).values(Annotate=1)
            session.execute(u)
            session.commit()

    else:
        u_id = df.iloc[rows,-3][r_index]
        print (u_id)
        loc = np.where(df.iloc[:,-3]==u_id)[0]
        print (loc)
        df.iloc[loc,-1] = 1
        df.to_csv("annotated.csv", sep = ',', index=False, encoding = 'utf8')
        
        
    
    
#%%
def function_to_call(attr, old, new):    
    cpu_job = select.value    
    src = create_source(cpu_job)
    source.data.update(src.data)
    print (cpu_job)    
    
    
def onclick_event(event):
    print('Python:Click')
    print (event.x)
    print (event.y)
    xclick = datetime.datetime.fromtimestamp(event.x/1e3)
    r_index = find_nearest(df.iloc[rows,-3],xclick)
    print (len(df.iloc[rows,-3]))
    print (r_index)
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




