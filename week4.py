#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 11:19:03 2020

@author: ggonecrane
"""

import pandas as pd
import numpy
import scipy
import seaborn
import matplotlib.pyplot as plt


#setting variables you will be working with to numeric
#converting income category to numeric
convert_param = 'float'

ICP = 'incomeperperson'
LE = 'lifeexpectancy'
AC = 'alcconsumption'
ALCONS_LEVEL = 'ALCONS_LEVEL'
AC_LEVEL_HIGH = 10
AC_LEVEL_MED = 6



def printTableLabel(label):
    print('\n')
    print('-------------------------------------------------------------------------------------')
    print(f'\t\t{label}')
    print('-------------------------------------------------------------------------------------')
    

def alcoholConsumptionLevel(row):
    val = float(row)
    if val <= AC_LEVEL_MED:
        return  1
    elif val  <= AC_LEVEL_HIGH:
        return 2
    elif val  > AC_LEVEL_HIGH:
        return 3
    
    
data = pd.read_csv('gapminder.csv', low_memory=False)

pd.to_numeric(data[ICP], downcast=convert_param, errors='coerce')
pd.to_numeric(data[LE], downcast=convert_param, errors='coerce')
pd.to_numeric(data[AC], downcast=convert_param, errors='coerce')

data[LE]=data[LE].replace(' ', numpy.nan)
data[ICP]=data[ICP].replace(' ', numpy.nan)
data[AC]=data[AC].replace(' ', numpy.nan)

data_clean = data.dropna().copy(deep=True)

data_clean[ICP] = data_clean[ICP].apply(lambda x: float(x))
data_clean[LE] = data_clean[LE].apply(lambda x: float(x))

data_clean[ALCONS_LEVEL] = data[AC].apply(lambda x: alcoholConsumptionLevel(x))
chk1 = data_clean[ALCONS_LEVEL].value_counts(sort=False, dropna=False)
printTableLabel('Alcohol Consumption Level')
print(chk1)

sub1 = data_clean[data_clean[ALCONS_LEVEL] == 1]
sub2 = data_clean[data_clean[ALCONS_LEVEL] == 2]
sub3 = data_clean[data_clean[ALCONS_LEVEL] == 3]    

printTableLabel('Association between Life Expectancy and Income per Person for LOW Alcohol Consumption Level')
print (scipy.stats.pearsonr(sub1[ICP], sub1[LE]))

printTableLabel('Association between Life Expectancy and Income per Person for MEDIUM Alcohol Consumption Level')
print (scipy.stats.pearsonr(sub2[ICP], sub2[LE]))

printTableLabel('Association between Life Expectancy and Income per Person for HIGH Alcohol Consumption Level')
print (scipy.stats.pearsonr(sub3[ICP], sub3[LE]))


############ Graphing with Scatter Plot ###########

scat = seaborn.regplot(x=LE, y=ICP, fit_reg=True, data=sub1)
plt.ylabel('Income per Person')
plt.xlabel('Life Expectancy')
plt.title('Income per Person and Life Expectancy for Low Alcohol Consumption Level')
plt.xlim(0, 100)
plt.ylim(0, 85000)
plt.show()

scat = seaborn.regplot(x=LE, y=ICP, fit_reg=True, data=sub2)
plt.ylabel('Income per Person')
plt.xlabel('Life Expectancy')
plt.title('Income per Person and Life Expectancy for Medium Alcohol Consumption Level')
plt.xlim(0, 100)
plt.ylim(0, 85000)
plt.show()

scat = seaborn.regplot(x=LE, y=ICP, fit_reg=True, data=sub3)
plt.ylabel('Income per Person')
plt.xlabel('Life Expectancy')
plt.title('Income per Person and Life Expectancy for High Alcohol Consumption Level')
plt.xlim(0, 100)
plt.ylim(0, 85000)
plt.show()


####################

"""data = pd.read_csv('gapminder.csv', low_memory=False)

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
"""