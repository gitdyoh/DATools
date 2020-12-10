#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 06:32:53 2020

@author: ggonecrane
"""

import pandas as pd
import numpy
import scipy.stats
import seaborn
import matplotlib.pyplot as plt

def printTableLabel(label):
    print('\n')
    print('-------------------------------------------------------------------------------------')
    print(f'\t\t{label}')
    print('-------------------------------------------------------------------------------------')

def printMedianIncomeLevelByRace():
    printTableLabel('Median Income Level by Race')
    w_median = sub1.groupby(race_col).get_group(1)[income_col].median()
    b_median = sub1.groupby(race_col).get_group(2)[income_col].median()
    o_median = sub1.groupby(race_col).get_group(3)[income_col].median()
    h_median = sub1.groupby(race_col).get_group(4)[income_col].median()
    m_median = sub1.groupby(race_col).get_group(5)[income_col].median()
    print(f'white: {w_median}, black: {b_median}, others: {o_median}, hispanic: {h_median}, mixed: {m_median}\n')

    
# load Outlook Life data set
data = pd.read_csv('OutlookLife.csv', low_memory=False)


df = pd.DataFrame(data)

# map table names to user friendly variable names
race_col = 'PPETHM'
income_col = 'W1_P20'
approx_annual_income = 'approx_annual_income'
BI_INC_LEVEL = 'BI_INC_LEVEL'

approx_income = {1: 2500, 2: 6250, 3: 8750, 4: 11250, 5: 13750, 6: 17500, 7: 22500,
                 8: 27500, 9:32500, 10: 37500, 11: 45000, 12: 55000, 13: 67500, 14: 80000,
                 15: 92500, 16: 112500, 17: 137500, 18: 162500, 19: 200000}

raceCode = {1: 'White', 2:'Black', 3: 'Other', 4: 'Hispanic', 5: 'Mixed'}

#converting income category to numeric
pd.to_numeric(df[income_col], downcast='signed', errors='coerce')

#subset data to exclude outliers - income category 1 and 19
#sub1=data[(data[income_col]>1) & (data[income_col]<19)].copy()
sub1=data[[income_col, race_col]].copy()
# replace invalid input to NaN
sub1[income_col] = sub1[income_col].replace(-1,numpy.nan)
# median income category of total population
median_inc_cat = int(sub1[income_col].median())

# a new variable categorize person's annual income higher than population median income or not
sub1[BI_INC_LEVEL] = sub1[income_col].apply(lambda x: 1 if x > median_inc_cat else 0)
sub1[approx_annual_income]= sub1[income_col].map(approx_income)
#converting new variable approx_annual_income to numeric
pd.to_numeric(sub1[approx_annual_income], downcast='signed', errors='coerce')

printTableLabel ('Median Income Level of Total Population')
print(f'income category: {median_inc_cat}')
print(f'approximated median income: {approx_income[median_inc_cat]}\n')

# contingency table of observed counts
ct1 = pd.crosstab(sub1[BI_INC_LEVEL], sub1[race_col])
ct1.columns = raceCode.values()
ct1.index = ['<= Median', '> Median']
printTableLabel ('Contingency Table of Observed Counts')
print (ct1)

# column percentages
colsum=ct1.sum(axis=0)
colpct=ct1/colsum
printTableLabel ('Contingency Table of Observed Percentages')
print(colpct)

# chi-square
printTableLabel ('Chi-Square Value, P-Value, Expected Counts')
cs1= scipy.stats.chi2_contingency(ct1)
print (cs1)

# set variable types 
sub1[race_col] = sub1[race_col].astype('category')
sub1[race_col].cat.rename_categories(raceCode.values(), inplace=True)

# new code for setting variables to numeric:
sub1[BI_INC_LEVEL] = pd.to_numeric(sub1[BI_INC_LEVEL], errors='coerce')

# graph percent with nicotine dependence within each smoking frequency group 
seaborn.catplot(x=race_col, y=BI_INC_LEVEL, data=sub1, kind="bar", ci=None)
plt.xlabel('Ethnicity')
plt.ylabel('Income Level against Population Median Income')

sub1[race_col].cat.rename_categories([1,2,3,4,5], inplace=True)


############# Chi-Square test on between group comparisions ##############

def runChiSqTestOnPairGroup(df, group1, group2):
    recode = {group1: group1, group2: group2}
    new_col_name = f'{raceCode[group1]} vs. {raceCode[group2]}'
    df[new_col_name]= df[race_col].map(recode)
    
    # contingency table of observed counts
    ct = pd.crosstab(df[BI_INC_LEVEL], df[new_col_name])
    printTableLabel (f'Contingency Table of Observed Counts ({new_col_name})')
    print (ct)
    
    # column percentages
    colsum=ct.sum(axis=0)
    colpct=ct/colsum
    printTableLabel (f'Contingency Table of Observed Percentages ({new_col_name})')
    print(colpct)

    printTableLabel (f'Chi-Square Value, P-Value, Expected Counts ({new_col_name})')
    cs= scipy.stats.chi2_contingency(ct)
    print (cs)


for i in [1, 2, 3, 4, 5]:
    for j in [1, 2, 3, 4, 5]:
        if j > i:
            runChiSqTestOnPairGroup(sub1, i, j)

