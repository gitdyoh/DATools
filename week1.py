#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 08:03:06 2020

@author: ggonecrane
"""

import pandas as pd
import numpy
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi 

g_raceCode1 = {1: 'White', 2:'Black', 3: 'Other', 4: 'Hispanic', 5: 'Mixed'}

g_incomeCode1 = {1: '<5K', 2:'5K-7.5K', 3: '7.5K-10K', 4: '10K-12.5K', 
                  5: '12.5K-15K', 6:'15K-20K', 7:'20K-25K', 8:'25K-30K',
                  9: '30K-35K', 10:'35K-40K', 11:'40K-50K', 12:'50K-60K',
                  13: '60K-75K', 14:'75K-85K', 15:'85K-100K', 16:'100K-125K',
                  17: '125K-150K', 18:'150K-175K', 19:'>175K'}

def printTableLabel(label):
    print('\n')
    print('-------------------------------------------------------------------------------------')
    print(f'\t\t\t\t{label}')
    print('-------------------------------------------------------------------------------------')

# load Outlook Life data set
data = pd.read_csv('OutlookLife.csv', low_memory=False)

df = pd.DataFrame(data)

# map table names to user friendly variable names
race_col = 'PPETHM'
income_col = 'W1_P20'
approx_annual_income = 'approx_annual_income'

#subset data to exclude outliers - income category 1 and 19
sub1=data[(data[income_col]>1) & (data[income_col]<19)].copy()
# replace invalid input to NaN
sub1[income_col] = sub1[income_col].replace(-1,numpy.nan)

approx_income = {1: 2500, 2: 6250, 3: 8750, 4: 11250, 5: 13750, 6: 17500, 7: 22500,
                 8: 27500, 9:32500, 10: 37500, 11: 45000, 12: 55000, 13: 67500, 14: 80000,
                 15: 92500, 16: 112500, 17: 137500, 18: 162500, 19: 200000}

sub1[approx_annual_income]= sub1[income_col].map(approx_income)
# printTableLabel('Personal Annual Income range')
print(sub1[[income_col, approx_annual_income]])

#converting new variable approx_annual_income to numeric
pd.to_numeric(sub1[approx_annual_income], downcast='signed', errors='coerce')

appr_inc1 = sub1.groupby(approx_annual_income).size()
printTableLabel('Approx. Income Size')
print (appr_inc1)

sub2 = sub1[[approx_annual_income, race_col]].dropna()

# using ols function for calculating the F-statistic and associated p value
model1 = smf.ols(formula='approx_annual_income ~ C(PPETHM)', data=sub2)
results1 = model1.fit()
printTableLabel('Result Summary')
print (results1.summary())
print('\n')

m2= sub2.groupby(race_col).mean()
printTableLabel('Means for Annual Income Estimate by Ethnicity')
print (m2)
print('\n')

sd2 = sub2.groupby(race_col).std()
printTableLabel('Standard Deviations for Annual Income Estimate by Ethnicity')
print (sd2)
print('\n')

mc1 = multi.MultiComparison(sub2[approx_annual_income], sub2[race_col])
res1 = mc1.tukeyhsd()
printTableLabel('Multi-comparison Result')
print(res1.summary())
