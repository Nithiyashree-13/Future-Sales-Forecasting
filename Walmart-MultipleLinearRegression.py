# -*- coding: utf-8 -*-
"""Walmart_salesforecast_externship.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-vX330VGBNpldQOJXXLHi1MNmaCsrzXZ

# **Walmart store salesforecasting**

**Dataset description:**

In this dataset, we have weekly sales data for 45 stores for a period of 3 years. In addition, we had store and geography specific information such as store size, unemployment rate, temperature etc

**stores.csv**

This file contains information about the 45 stores, indicating its type and size of store.(type defines whether the store is of type A,B,C and size defines no.of products in the store)

**features.csv**

This file contains additional data related to the store and regional activity for the given dates. It contains the following fields:

Store - the store number

Date - the week

Temperature - average temperature in the region

Fuel_Price - cost of fuel in the region

CPI - the consumer price index

Unemployment - the unemployment rate

IsHoliday - whether the week is a special holiday week

# New Section

**Data extraction**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

import seaborn as sns

from google.colab import drive
drive.mount('/content/drive')

features=pd.read_csv("/content/drive/MyDrive/Colab Notebooks/features.csv")
store=pd.read_csv("/content/drive/MyDrive/Colab Notebooks/stores.csv")
train=pd.read_csv("/content/drive/MyDrive/Colab Notebooks/train.csv")
test=pd.read_csv("/content/drive/MyDrive/Colab Notebooks/test.csv")
features.head()

"""**Data Preprocessing**

Taking important information and merging the data
"""

train=train.groupby(['Store','Date'])['Weekly_Sales'].sum()
train=train.reset_index()
train.head(10)

data=pd.merge(train,features,on=['Store','Date'],how='inner')
data.head(10)

data=pd.merge(data,store,on=['Store'],how='inner')
data.head()

"""Sorting based on date"""

data=data.sort_values(by='Date')
data.head(10)

"""Removing unwanted features from the dataframe"""

data=data.drop(['MarkDown1','MarkDown2','MarkDown3','MarkDown4','MarkDown5'],axis=1)
data.head(10)

data.shape

"""**Checking for null values and verify that data is clean.**"""

data.isnull().sum()

"""**Converting IsHoliday (which is string) into Holiday (which is integer) 1 for holiday and 0 otherwise.**"""

data['Holiday']=[int(i) for i in list(data.IsHoliday)]
data.head()

"""**Splitting store type into categorical features.**

As we have 3 types of stores (A,B and C) which are categorical. Therefore splitting each type as a feature into one-hot encoding

(we know of both columns B and C are 0 then it is A-type. So B=1 and C=0 for B.B=0 and C=1 for C.B=0 and C=0 for A)
"""

Type_dummy=pd.get_dummies(data['Type'],drop_first=True)
Type_dummy.head(10)

data=pd.concat([data,Type_dummy],axis=1)
data.head(10)

"""
**Manipulating data.**

 Transform data into useful information and deleting unnecessary items. Getting the final data."""

data=data.drop(['Type','IsHoliday'],axis=1)
data.drop(10)

"""**Splitting data into train and test data. The size of the test data is 20%.**"""

X=data.drop(['Weekly_Sales','Store','Date'],axis=1)
y=data['Weekly_Sales']
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
X.head()

"""**Applying linear regression and fit the training data into it.**"""

LR=LinearRegression(normalize=True)
LR.fit(X_train,y_train)

"""**Predicting the data for test value as per linear regression.**"""

y_pred=LR.predict(X_test)
y_pred

"""**Data visualization**"""

y_pred=LR.predict(X_test)
plt.plot(y_test,y_pred,'ro')
plt.plot(y_test,y_test,'b-')
plt.show()

"""**Evaluating the model by calculating errors by the root mean square error and R - squared.**"""

Root_mean_square_error=np.sqrt(np.mean(np.square(y_test-y_pred)))
print(Root_mean_square_error)

from sklearn.metrics import r2_score
r2=r2_score(y_test,y_pred)
print(r2)

acc_lr= round(LR.score(X_train,y_train) * 100, 2)
print ("Accuracy:",acc_lr)

"""To predict the weekly sales,we give particular tuple to input in the model and predict the weekly sales as output
Final prediction
"""

prediction=LR.predict(pd.DataFrame([(40.37,2.876,173.325456,7.934,103464,0,0,0)]))
print(prediction)