#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 17:46:53 2017

@author: anand
"""
#%%
import itertools
import numpy as np
import pandas as pd
import sklearn as sk
from sklearn import linear_model
from sklearn import svm
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier



#%%
df = pd.read_csv('annotated.csv', sep = ',')
df['Annotate'] = df['Annotate'].astype(int)

#%%

X = np.column_stack((df['JOB_NAME'],df['MSU_CPU'],df['Z_Score'],df['Scaled'],df['Rolling']))
Y= df.iloc[:,-1].values

X_train,X_test,Y_train,Y_test = train_test_split(X[:,1:],Y,random_state=0) 


#%%SVM
svc = svm.SVC(kernel='rbf')
svc.fit(X_train,Y_train)

print("accuracy=",sk.metrics.accuracy_score(Y_test,svc.predict(X_test)))
print("precision=",sk.metrics.precision_score(Y_test,svc.predict(X_test),average='binary'))

labels = [0,1]
cm = sk.metrics.confusion_matrix(Y_test,svc.predict(X_test),labels)
print("confusion matrix=")

print(cm)

#%%Logistic Regression
#==============================================================================
# reg = linear_model.LogisticRegression()                                                #Logistic Regression
# reg.fit(X_train,Y_train)                                                               #Logistic Regression
# print("accuracy=",sk.metrics.accuracy_score(Y_train,reg.predict(X_train)))
# 
# print("precision=",sk.metrics.precision_score(Y_train,reg.predict(X_train),average='binary'))
#==============================================================================

#%%MLP
# =============================================================================
# mlp = MLPClassifier(alpha=0.01)
# mlp.fit(X_train,Y_train)
# 
# print("accuracy=",sk.metrics.accuracy_score(Y_test,mlp.predict(X_test)))
# print("precision=",sk.metrics.precision_score(Y_test,mlp.predict(X_test),average='binary'))
# 
# labels = [0,1]
# cm = sk.metrics.confusion_matrix(Y_test,mlp.predict(X_test),labels)
# print("confusion matrix=")
# 
# print(cm)
# =============================================================================


#%%
fig1 = plt.figure(1)
ax = fig1.add_subplot(111)
cax = ax.matshow(cm)
for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    ax.text(j,i,cm[i,j])
plt.title('Confusion matrix of the classifier')
fig1.colorbar(cax)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels)
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

#%%
rows = np.where(X[:,0]=="CTD001AH")[0]
data = X[rows,1:]
arr = svc.predict(data)

#%%
plt.figure(figsize=(12,10))
plt.subplot(2,1,1)
plt.plot(data[:,-1])
count = 0
for i in xrange(len(arr)-1):
    if (arr[i] != arr[i+1]):
        count += 1
        plt.axvline(i, color='#FF4E24', ls='dotted',lw=1.0)
        
               
plt.subplot(2,1,2)
plt.plot(arr, color='r')

