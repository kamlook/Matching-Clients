# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 11:38:50 2020

@author: Kam Look
"""

import numpy as np
import pandas as pd

NaN = np.nan
dictionary = {'one':[10,20,30,40,50],'two': ['blue','red','blue','blue','red']}
df = pd.DataFrame(dictionary)

df['three'] = np.where(df['one'] >=40,'high',np.where(df['one']>= 20, 'medium','low'))
df['four'] = [1,2,3,4,5]
testList = ['low','medium']


dictionary['one'] =[10,20,25,40,50]
df2 = pd.DataFrame(dictionary)
mergedStuff = pd.merge(df, df2, on=['one'], how='inner')

'''
Long list of Kimo's Desired Jobs
# note! is this a comprehensive list??

dir_mang_jobs = ['City Clerk/Director',
                 'Director of Public Works',
                 'Planning Director',
                 'Director of Finance',
                 'Asst Director of Community Services',
                 'Assistant Planning Director',
                 'Director of Community Services',
                 'Director of Utilities',
                 'Library Director',
                 'Director of Community Dev',
                 'Deputy Director of Utilities',
                 'Assistant Finance Director',
                 'Interim Hr Director',
                 'Director of Community Development',
                 '',
                 '',
                 ''
                 ]
'''

