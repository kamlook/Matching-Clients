# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:01:53 2020

@author: Kam Look
"""
import os
import pandas as pd

pathCA = r'D:\PPI Matching Names\Cities'
pathBond = r'D:\PPI Matching Names\BondAdaptPeople-Data.csv'

def parse_transparent_data(pathCA):
    '''
    input: path = directory path to folder of folders as a string
    '''
    ### OPENING AND READING COLLECTION OF FILES ###
    masterDF = pd.DataFrame(columns = ['Employee Name','Job Title','Base Pay', 'Agency'])
    
    for dirName, subDirList, fileList in os.walk(pathCA, topdown = True):
        # print('Found Directory: {}'.format(dirName))
        if fileList != []:
            if fileList[-1].find('.csv') == -1: # making sure all files being used are csv
                print('All Files must be a .csv!')
                break
            #  state file path and read the most up to date csv file 
            # print(dirName + "\\"  + fileList[-1])
            tempDF = pd.read_csv(dirName + "\\"  + fileList[-1], usecols = ['Employee Name','Job Title','Base Pay','Agency']) 
            masterDF = pd.concat([masterDF,tempDF], ignore_index = True) # concatinate all files to one big data frame 
        else:pass 
    
    ### IDENTIFYING UNIQUE JOB TITLES AND ONLY KEEPING ONES USEFUL O PPI
    # i.e: Monique S Willis is listed twice doing the same job but getting two forms of pay
    jobTitles=masterDF['Job Title'].unique()
    necsJobs_list = ['Eng','Tech','Human', 'HR']
    unnecsJobs_list = ['Police', 'Fire', 'Pool', 'Intern', 'Video' ,'Graphics','Temp'] # add intern
    nescJobs = []
    # keep useful jobs
    for jobs in jobTitles:
        for keepers in necsJobs_list:
            if keepers in jobs:
                nescJobs.append(jobs)
    # continue removing unnecessary jobs         
    for jobs in nescJobs:
        for removes in unnecsJobs_list:
            #try removing job, but if job doesnt exist, just pass error
            #i.e if "police officer temp" already removed, when temp is checked it wont break
            if removes in jobs:
                try:
                    nescJobs.remove(jobs)
                except ValueError:
                    pass
                
    ### GROUP PEOPLE BASED ON PAY ###
    # next do do item 
    
                
    '''
    dfDupes = masterDF[masterDF.duplicated()] # create df of duplicate data
    dfDupes=dfDupes.rename(columns={'Employee Name':'EmpName','Job Title': 'JobTitle', 'Base Pay':'BasePay'}) # rename column to remove space
    useless_entries = ['Not Provided', 'Redacted', 'Withheld Name']
    dfNA = pd.DataFrame(columns = ['EmpName','JobTitle','BasePay', 'Agency']) # keep all withheld names 
    for names in useless_entries:
        dfNA_temp= dfDupes[dfDupes.EmpName == names]
        dfNA = pd.concat([dfNA,dfNA_temp], ignore_index = True)
        dfDupes = dfDupes[dfDupes.EmpName != names] # duplicate names 
    
    '''
    return masterDF, nescJobs

def parse_bond_data(pathBond):
    '''
    input: path directly to bond csv
    '''
    bondDF = pd.read_csv(pathBond, usecols = ['1 Name Alphanumeric','2 First_Name Alphanumeric', '20 City Alphanumeric', '37 Last Name Alphanumeric'])
    
    return bondDF
