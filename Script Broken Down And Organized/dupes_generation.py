# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 15:16:01 2020

@author: Kam Look
"""
import pandas as pd

pathBond = r'D:\PPI Matching Names\BondAdaptPeople-Data.csv'

bondDF = pd.read_csv(pathBond, usecols = ['UniqueID','1 Name Alphanumeric','2 First_Name Alphanumeric','18 Address1 Alphanumeric','36 Nickname Alphanumeric',
                                              '37 Last Name Alphanumeric','41 Job Title Alphanumeric',
                                              '44 Employer Xref'])
bondDupes = bondDF[bondDF.duplicated(subset=['2 First_Name Alphanumeric','37 Last Name Alphanumeric'],  keep=False)]
bondNames = split_full_name(bondDupes)
bondNames = address_split(bondNames)
confirmDupes = bondNames[bondNames.duplicated(subset=['2 First_Name Alphanumeric','37 Last Name Alphanumeric', 'Middle Stuff'], keep=False)]
bondNames = bondNames[~bondNames.duplicated(subset=['2 First_Name Alphanumeric','37 Last Name Alphanumeric', 'Middle Stuff'], keep=False)]
sameAddress = bondNames[bondNames.duplicated(subset=['2 First_Name Alphanumeric','37 Last Name Alphanumeric', 'Home Address'], keep=False)]
confirmDupes=confirmDupes.append(sameAddress)
bondNames = bondNames[~bondNames.duplicated(subset=['2 First_Name Alphanumeric','37 Last Name Alphanumeric', 'Home Address'],keep=False)]


bondNames.to_csv('BondDupes_toBeChecked_July28.csv',index=False)
confirmDupes.to_csv('confirmedDupes_July28.csv', index=False)

# used on each row as part of a .apply()