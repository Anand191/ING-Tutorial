#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 11:17:28 2017

@author: anand
"""

#%%
import itertools
import numpy as np
import pandas as pd
import sklearn as sk
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV


#%%
df = pd.read_csv('annotated.csv', sep = ',')
df['Annotate'] = df['Annotate'].astype(int)

#%%

X = np.column_stack((df['JOB_NAME'],df['MSU_CPU'],df['Z_Score'],df['Scaled'],df['Rolling']))
Y= df.iloc[:,-1].values
svc = GridSearchCV(svm.SVC(kernel='rbf', gamma = 0.1 ), cv=2,
                   param_grid={"C":[1e0,1e1,1e2],
                               "gamma": np.logspace(-2,2,5)})

jobs = np.unique(X[:,0])

#%%
def classify(rows):
    
    X_train,X_test,Y_train,Y_test = train_test_split(X[rows,1:],Y[rows],random_state=0, stratify = Y[rows])

    svc.fit(X_train,Y_train)
    
    print("accuracy=",sk.metrics.accuracy_score(Y_test,svc.predict(X_test)))
    print("precision=",sk.metrics.precision_score(Y_test,svc.predict(X_test),average='binary'))
    
    labels = [0,1]
    cm = sk.metrics.confusion_matrix(Y_test,svc.predict(X_test),labels)
    print("confusion matrix=")    
    print(cm)
    
    fig1 = plt.figure(figsize=(12,10))
    ax = fig1.add_subplot(211)
    cax = ax.matshow(cm)
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax.text(j,i,cm[i,j])
    plt.title('Confusion matrix of the classifier')
    fig1.colorbar(cax)
    ax.set_xticklabels([''] + labels)
    ax.set_yticklabels([''] + labels)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    
    
    ax1 = fig1.add_subplot(2,1,2)
    data = X[rows,1:]
    xcoord = np.arange(len(data))
    arr = svc.predict(data)    
    sc = ax1.scatter(xcoord,data[:,-1], c=arr)
    plt.colorbar(sc)
    
# =============================================================================
#     count = 0
#     for i in xrange(len(arr)-1):
#         if (arr[i] != arr[i+1]):
#             count += 1
#             ax1.axvline(i, color='#FF4E24', ls='dotted',lw=1.0)
# =============================================================================
    plt.show()
    print("\n")



#%%SVM
for job in jobs:
    rr = np.where(X[:,0]==job)[0]
    classify(rr)
    
    






