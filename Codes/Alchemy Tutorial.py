#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 17:09:18 2017

@author: anand
"""
#%%
from time import time
from datetime import datetime
from sqlalchemy import Column, Integer, Float, Date, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd

Base = declarative_base()
#%%
class cdb1(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'cdb1'
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    id = Column(Integer, primary_key=True, nullable=False) 
    FK_DateKey = Column(DateTime)
    Time = Column(DateTime)
    MVS_SYSTEM_ID = Column(String(250))
    JOB_NAME = Column(String(250))
    MSU_CPU = Column(Float)
    
#%%
engine = create_engine('sqlite:///cdb.db')
Base.metadata.create_all(engine)

df = pd.read_csv('CPU50.csv')
df.to_sql(con=engine, index_label='id', name=cdb1.__tablename__, if_exists='replace')
 