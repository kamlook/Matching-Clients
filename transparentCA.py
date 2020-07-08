# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:01:53 2020
@author: Kam Look
"""
import os
import datetime
import numpy as np
import pandas as pd

# write paths for testing into easily testable variables

pathCA = r'D:\PPI Matching Names\Cities'
pathBond = r'D:\PPI Matching Names\BondAdaptPeople-Data.csv'

pathConstruct = r'D:\PPI Matching Names\PossibleJobs\construction.csv'
pathEng1 = r'D:\PPI Matching Names\PossibleJobs\engineer1.csv'
pathEngSupp = r'D:\PPI Matching Names\PossibleJobs\Engineering Support.csv'
pathPlanning = r'D:\PPI Matching Names\PossibleJobs\planning.csv'
pathHR = r'D:\PPI Matching Names\PossibleJobs\HR.csv'

paths = [pathConstruct, pathEng1, pathEngSupp, pathPlanning, pathHR] # will be iterated through

#def open_trans_data(pathCA):
def parse_transparent_data(pathCA,paths):
    '''
    input: path = directory path to folder of folders as a string
    '''
    beginTime  = datetime.datetime.now()
    
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
    convertTime = datetime.datetime.now()
    
    ### IDENTIFYING UNIQUE JOB TITLES AND ONLY KEEPING ONES USEFUL TO PPI ###
    # note as of July 6th, the parsing has not yet been aplied to the masterDF, still generating a list of relevant jobs 
    jobTitles=masterDF['Job Title'].unique()
    necsJobs_list = get_unique_jobs(paths) # beware, not as limiting as you may think. i.e analyst, manager
    unnecsJobs_list = ['Police', 'Fire', 'Pool', 'Intern', 'Park', 'Video' ,
                       'Graphics','Temp', 'Ztemp','Airport','Admin',
                       'Recreation','Library', 'Finance','Sport','Farm','Hous',
                       'Analyst', 'Aqua', 'Crime', 'Legis', 'Cement',
                       'Forensic', 'Custodian', 'Arts','Kids','Child', 'Peace', 'Homework',
                       'Battalion','Neighborhood','Ambulance', 'Emergency','Learning','Nutrition',
                       'Payroll', 'Coach', 'Public Sfty', 'Equip Oper', 'Cultur', 'Operator',
                       'Budget', 'Collector']
    nescJobs = []
    
    # keep useful jobs
    for jobs in jobTitles:
        for keepers in necsJobs_list:
            if keepers in jobs:
                nescJobs.append(jobs)
                
    # continue removing unnecessary jobs  
    
    for jobs in nescJobs.copy(): # error before came from editing list while iterating through it 
        for removes in unnecsJobs_list:
            # try removing job, but if job doesnt exist, just pass error
            # i.e if "police officer temp" already removed, when temp is checked it wont break
            
            if removes in jobs:
                # print('{} and {}'.format(removes, jobs))
                try:
                    nescJobs.remove(jobs)
                except ValueError:
                    pass
                
    nescJobs = set(nescJobs) # make only unique
    jobsDF = masterDF[masterDF['Job Title'].isin(nescJobs)]
    #saving list to a csv for Kimo
    #printDF = pd.DataFrame(nescJobs, columns=['Job Titles'])
    #printDF.to_csv('jobTitles.csv',index=False)
    
    ### GROUP PEOPLE BASED ON PAY ###
    sortTime = datetime.datetime.now()
    topCutoff = 89999
    midCutoff = 9999
    #search through df with essentially an "if else" statement 
    jobsDF['Pay Bracket'] = np.where(jobsDF['Base Pay'] > topCutoff, 'High',
            np.where(jobsDF['Base Pay'] > midCutoff, 'Middle', 'Low'))
    jobsDF = jobsDF.reset_index(drop=True)
    
    
    ### SPLITTING FULL NAME INTO PARTS###
    ### CHECKING RUNTIMES ###
    # my excuse for keeping it in one big file
    print('Reading Time: {}'.format(convertTime - beginTime))
    print('Sorting Time: {}'.format(sortTime - convertTime))
    print('Total time: {}'.format(datetime.datetime.now() - beginTime))
    
    # previously I have wanted masterDF,  nescJobs, and jobsDF
    return masterDF, jobsDF

def parse_bond_data(pathBond):
    '''
    input: path directly to bond csv
    '''
    
    # only using first and last names, not even middle names 
    bondDF = pd.read_csv(pathBond, usecols = ['2 First_Name Alphanumeric','36 Nickname Alphanumeric', '37 Last Name Alphanumeric'])
    # we need astype(str) to convert pd.Series object into a str
    bondDF['Full Name'] = bondDF[['2 First_Name Alphanumeric', '37 Last Name Alphanumeric']].apply(lambda full: ' '.join(full.astype(str)),axis=1)



    return bondDF

def get_unique_jobs(paths):
    uniqueJobs=[]
    for file_path in paths:
        # print(file_path)
        temp_jobDF = pd.read_csv(file_path, usecols= ['JobTitle'], encoding="ISO-8859-1")
        tempUnique = temp_jobDF['JobTitle'].unique()
        uniqueJobs=uniqueJobs+ list(tempUnique) # add unique jobs to master list 
    uniqueJobsClean = [x for x in uniqueJobs if str(x) != 'nan']
    return uniqueJobsClean

def split_full_name(jobsDF):
    # make a series of List of the employees full names
    peopleSeries = jobsDF['Employee Name'].str.split(expand = False)
    suffix = ['jr','jr.','ii','iii']
    firstName = []
    lastName =[] # Last Yucca Valley people really threw the data for a loop. do them manually or just drop them? 
    middleIn = []
    extras = []
    tempSuffix =[]
    # making lists then adding the list to the dataframe straight away, no need to convert to series df['List']=list
    
    for nameList in peopleSeries:
        #jr and ending check
        if nameList[-1].lower() in suffix:
            while nameList[-1].lower() in suffix:
                tempSuffix.append(nameList.pop(-1))
                tempAdd = ' '.join(tempSuffix)
            extras.append(tempAdd)
            tempSuffix = []
        else:
             extras.append('')
        # last name grabbed before first name, sometimes first name is missing
        lastName.append(nameList.pop(-1))
        #check if first name exists, if so append it 
        if nameList != []:
            firstName.append(nameList.pop(0))
        else:
            firstName.append('N/A')
        # throw all middle initials in names in big middle list
        middleIn.append(' '.join(nameList))
    jobsDF['First Name','Middle Stuff']=firstName
    jobsDF['Middle Stuff']=middleIn
    jobsDF['Last Name']=lastName
    jobsDF['Extras']=extras
    
    return jobsDF
        

# peopleDF = bondDF
# transDF = jobsDF
def compare_dataframes(peopleDF, transDF):
    transDF['Full Name'] = transDF['Employee Name']
    mergedDF = pd.merge(peopleDF, transDF, on=['Full Name'], how='right',indicator=True)
    
    return mergedDF
    
def main(pathCA, pathBond, paths):
    '''
    INPUTS
    str     pathCA: path to directory with Transparent California Files
    str     pathBond: path to Bond-People csv
    list    paths: list of paths bond files with unique job titles
    '''
    
    _, jobsDF = parse_transparent_data(pathCA,paths)
    bondDF = parse_bond_data(pathBond)
    merged = compare_dataframes(bondDF, jobsDF)
    merged_trans_only=merged[merged['_merge']=='right_only']
    merged_trans_only=merged_trans_only[['Employee Name','Job Title','Agency','Pay Bracket', '_merge']]
    merged_trans_only=merged_trans_only[merged_trans_only['Pay Bracket'] != 'Low']
    
    return merged_trans_only

    
    
    
    