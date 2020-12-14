#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 07:18:00 2020

@author: ggonecrane
"""

import pandas as pd
import numpy
import seaborn
import scipy
import matplotlib.pyplot as plt


def printTableLabel(label):
    print('\n')
    print('-------------------------------------------------------------------------------------')
    print(f'\t\t{label}')
    print('-------------------------------------------------------------------------------------')
    
    
data = pd.read_csv('gapminder.csv', low_memory=False)

#setting variables you will be working with to numeric
#converting income category to numeric
convert_param = 'float'

ICP = 'incomeperperson'
LE = 'lifeexpectancy'

pd.to_numeric(data[ICP], downcast=convert_param, errors='coerce')
pd.to_numeric(data[LE], downcast=convert_param, errors='coerce')

data[LE]=data[LE].replace(' ', numpy.nan)
data[ICP]=data[ICP].replace(' ', numpy.nan)

data_clean = data.dropna().copy(deep=True)

data_clean[ICP] = data_clean[ICP].apply(lambda x: float(x))
data_clean[LE] = data_clean[LE].apply(lambda x: float(x))


printTableLabel('Association between Life Expectancy and Income per Person')
print (scipy.stats.pearsonr(data_clean[ICP], data_clean[LE]))

############ Graphing with Scatter Plot ###########

scat = seaborn.regplot(x="lifeexpectancy", y="incomeperperson", fit_reg=True, data=data_clean)
plt.ylabel('Income per Person')
plt.xlabel('Life Expectancy')
plt.title('Scatterplot for the Association Between Income per Person and Life Expectancy')
plt.xlim(0, 100)
plt.ylim(0, 85000)
plt.show()

