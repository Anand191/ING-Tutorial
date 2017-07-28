#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 12:25:22 2017

@author: anand
"""

#%%
import pandas as pd
import numpy as np
from datetime import datetime
import os

dir = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(dir,'CPU50.csv'),sep=",")
df['TIME'] = df['TIME'].apply(lambda x: x.split('.')[0])
df['TIMESTAMP'] = df['FK_DateKey'].astype(str) + " " + df['TIME'].astype(str)
df.iloc[:,-1] = pd.to_datetime(df.iloc[:,-1])
df['U_ID'] = df['JOB_NAME'].astype(str) + "_" + df['TIMESTAMP'].astype(str)
df['Annotate'] = np.zeros(df.shape[0]) 
df = df.sort_values(by=['TIMESTAMP'])
#df.to_csv('chk.csv',sep=',',encoding='utf8')
jobs = df.iloc[:,3].unique().tolist()

#%%Create db
from time import time
from sqlalchemy import Column, Integer, Float, Date, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class cdb1(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'cdb1'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer) 
    FK_DateKey = Column(DateTime)
    Time = Column(DateTime)
    MVS_SYSTEM_ID = Column(String(250))
    JOB_NAME = Column(String(250))
    MSU_CPU = Column(Float)
    TIMESTAMP = Column(String(250))
    U_ID = Column(String(250), primary_key=True, nullable=False)
    Annotate = Column(Integer)
    

engine = create_engine('sqlite:///cdb.db')
Base.metadata.create_all(engine)

df.to_sql(con=engine, index_label='id', name=cdb1.__tablename__, if_exists='replace')