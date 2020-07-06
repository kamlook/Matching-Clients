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

# Creating the DataFrame 
df = pd.DataFrame({'Date':['10/2/2011', '11/2/2011', '12/2/2011', '13/2/2011'], 
					'Event':['Music', 'Poetry', 'Theatre', 'Comedy'], 
					'Cost':[10000, 5000, 15000, 2000]}) 

# Create a new column 'Discounted_Price' after applying 
# 10% discount on the existing 'Cost' column. 

# create a new column 
df['Discounted_Price'] = df['Cost'] - (0.1 * df['Cost']) 

# Print the DataFrame after 
# addition of new column 
print(df) 
