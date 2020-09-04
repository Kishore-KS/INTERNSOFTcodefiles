# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Importing the data set
adv_data = pd.read_csv("advertising.csv")
adv_data.head()

#Quick look into the data
adv_data.describe()
adv_data.info()

#Plotting
fig, axs = plt.subplots(1,3,sharey=True, figsize=(10,6))
for i, var in enumerate(adv_data.columns[:-1]):
    adv_data.plot(kind='scatter',x=var,y='Sales',ax=axs[i])

#Importing sci-kit learn
from sklearn.linear_model import LinearRegression

#uni-variable Linear Regression
print("Uni-Variate Linear Regression Model")

X = adv_data[['TV']]
y = adv_data[['Sales']]

ulr = LinearRegression()
ulr.fit(X, y)

print("\tIntercept: ",ulr.intercept_,"\n\tCo-efficient: ",ulr.coef_)

ulr.predict(pd.DataFrame({'TV':[65.2, 45.3, adv_data.TV.min(), adv_data.TV.max()]}))

#Plotting best fitting line
sns.lmplot(x='TV', y='Sales', data=adv_data)

#multi-variate Linear Regression
print("Multi-Variate Linear Regression Model: ")

mX = adv_data[['TV', 'Radio', 'Newspaper']]
my = adv_data[['Sales']]

mlr = LinearRegression()
mlr.fit(mX, my)

print("\tIntercept: ",mlr.intercept_,"\n\tCo-efficient: ",mlr.coef_)

#Importing stats
import statsmodels.formula.api as smf

#Evaluating ulr model
ulm = smf.ols(formula = 'Sales ~ TV', data=adv_data).fit() 
ulm.conf_int()
print("\nUni-variate Linear Regression Evaluation: \n")
print(ulm.summary())

#Evaluating mlr model
mlm = smf.ols(formula = 'Sales ~ TV+Radio+Newspaper', data=adv_data).fit() 
mlm.conf_int()
print("\nMulti-variate Linear Regression Evaluation: \n")
print(mlm.summary())


