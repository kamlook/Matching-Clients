# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 15:09:55 2020

@author: Kam Look
"""

import pandas as pd 

AllPeople = pd.read_csv(r'C:\Users\Kam Look\Desktop\Kimo Files\AllPeople.csv',encoding="ISO-8859-1")
Dupes = pd.read_csv(r'C:\Users\Kam Look\Desktop\Kimo Files\DupesToBeRemoved.csv',encoding="ISO-8859-1")

mergedDF = pd.merge(AllPeople,Dupes, how='left', on=['First Name','Last Name'], indicator='Only want left?')
mergedDF=mergedDF[mergedDF['Only want left?']=='left_only']