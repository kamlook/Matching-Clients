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

paths = [pathPlanning, pathHR, pathConstruct, pathEngSupp, pathEng1] # will be iterated through    
    
def parse_transparent_data(pathCA,paths=None):
    '''
    input: path = directory path to folder of folders as a string
    '''
    beginTime  = datetime.datetime.now()
    ## OPENING AND READING COLLECTION OF FILES ##
    masterDF = open_trans_data(pathCA)  
    convertTime = datetime.datetime.now()
    ##  GETTING PEOPLE WITH USEFUL JOBS ##
    nescJobs, jobsDF = get_jobsDF(masterDF,paths)
    sortTime = datetime.datetime.now()
    ## GROUP PEOPLE BASED ON PAY ##
    jobsDF = split_pay(jobsDF)
    ### SPLITTING FULL NAME INTO PARTS###
    jobsDF = split_full_name(jobsDF)
    ### CHECKING RUNTIMES ###
    print('Reading Time: {}'.format(convertTime - beginTime))
    print('Sorting and Selecting Time: {}'.format(sortTime - convertTime))
    print('Total time: {}'.format(datetime.datetime.now() - beginTime))
    # previously I have wanted masterDF,  nescJobs, and jobsDF
    return masterDF, jobsDF

def open_trans_data(pathCA):
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
    return masterDF

def get_jobsDF(masterDF,paths=None):
    ### IDENTIFYING UNIQUE JOB TITLES AND ONLY KEEPING ONES USEFUL TO PPI ###
    jobTitles=masterDF['Job Title'].unique()
    necsJobs_list = get_unique_jobs(paths) # beware, not as limiting as you may think. i.e analyst, manager
    unnecsJobs_list = [' - hr','-hr', 'account', 'administrative a', 'administrative c', 'administrative h', 'administrative l',
                     'administrative spec', 'administrative supp', 'administrative t', 'administrato',
                     'airport', 'ambulance', 'aqua', 'arts', 'athletic', 'attorney', 'battalion', 'budget',
                     'cement', 'child', 'clerk', 'climate', 'coach', 'collector', 'compliance',
                     'contract', 'controller', 'crime', 'cultur', 'custodian', 'economic', 'emergency',
                     'equip oper', 'farm', 'finance', 'fire', 'fiscal', 'forensic', 'forestry', 'graphics',
                     'homework', 'hous', 'hrly', 'intern', 'jr systems', 'kids', 'learning', 'legis',
                     'library', 'neighborhood', 'network', 'nutrition', 'operator', 'park', 'payroll', 'peace',
                     'personnel board', 'police', 'pool', 'pts office', 'public sfty', 'recreation', 'safety',
                     'secr', 'ser ', 'sport', 'sustainability', 'temp', 'test admin', 'tourism', 'transit',
                     'video', 'ztemp'] #blacklisted terms
    nescJobs = []
    # keep useful jobs
    for jobs in jobTitles:
        for keepers in necsJobs_list: # important because it checks if substring exists in string 
            if keepers in jobs:
                nescJobs.append(jobs)   
                
    # use blacklist to remove unnecessary jobs   
    for jobs in nescJobs.copy(): # error before came from editing list while iterating through it 
        for removes in unnecsJobs_list:
            # try removing job, but if job doesnt exist, just pass error
            # i.e if "police officer temp" already removed, when temp is checked it wont break           
            if removes in jobs.lower():
                try:
                    nescJobs.remove(jobs)
                except ValueError:
                    pass   
    nescJobs = set(nescJobs) # make nescJobs unique
    jobsDF = masterDF[masterDF['Job Title'].isin(nescJobs)]
    jobsDF = jobsDF.reset_index(drop=True)
    return nescJobs, jobsDF

def get_unique_jobs(paths=None):
    uniqueJobs=[]
    xFilter_lol = [] # list of lists 
    # read through given bond files to find all bond jobs in the database
    options = ['1', 'planners', 'plan','2','hr','3','construction',
               '4', 'engineering support','5','engineering 1',
               '6','no extra filter','none','no']
    if paths == None:
        print('As of July 9th, HR jobs is test by default')
        HR_jobs = ['Human Resources','HR','Hr','Personnel','Administ','Benefits Coordinator']
        filteredJobs = HR_jobs
        
    elif type(paths) == list:
        print('Using input file paths')
        for file_path in paths:
            # print(file_path)
            temp_jobDF = pd.read_csv(file_path, usecols= ['JobTitle'], encoding="ISO-8859-1")
            tempUnique = list(temp_jobDF['JobTitle'].unique())
            tempUnique = [x for x in tempUnique if str(x) != 'nan']
            xFilter_lol.append(tempUnique)
            uniqueJobs=uniqueJobs+ tempUnique # add unique jobs to master list
        print('1: Planners')
        print('2: HR')
        print('3: Construction')
        print('4: Engineering Support')
        print('5: Engineering 1')
        print('6: No extra filter')
        extraFilter=input('Choose extra filter from selection above: ')
        while extraFilter not in options:
            extraFilter = input('Please choose from one of the 6 options listed above: ')
            
        if extraFilter in options[0:3]:
            filteredJobs = xFilter_lol[0]
        elif extraFilter in options[3:5]:
            filteredJobs = xFilter_lol[1]
        elif extraFilter in options[5:7]:
            filteredJobs = xFilter_lol[2]
        elif extraFilter in options[7:9]:
            filteredJobs = xFilter_lol[3]
        elif extraFilter in options[9:11]:
            filteredJobs = xFilter_lol[4]
        elif extraFilter in options[11:-1]:
            filteredJobs = uniqueJobs
        
    # output filtered jobs 
    return filteredJobs

def split_pay(jobsDF):
    ### SPLITTING PAY INTO 3 BRACKETS ###
    topCutoff = 89999
    midCutoff = 49999
    #search through df with essentially an "if else" statement 
    jobsDF['Pay Bracket'] = np.where(jobsDF['Base Pay'] > topCutoff, 'High',
            np.where(jobsDF['Base Pay'] > midCutoff, 'Middle', 'Low'))
    return jobsDF


def parse_bond_data(pathBond):
    '''
    input: path directly to bond csv
    '''
    
    # only using first and last names, not even middle names 
    bondDF = pd.read_csv(pathBond, usecols = ['2 First_Name Alphanumeric','36 Nickname Alphanumeric', '37 Last Name Alphanumeric'])
    # we need astype(str) to convert pd.Series object into a str
    bondDF['Full Name'] = bondDF[['2 First_Name Alphanumeric', '37 Last Name Alphanumeric']].apply(lambda full: ' '.join(full.astype(str)),axis=1)
    
    return bondDF

# peopleDF = bondDF
# transDF = jobsDF
def compare_dataframes(peopleDF, transDF):
    transDF['Full Name'] = transDF['Employee Name']
    #Split names alrady happened in parse_trans_data!!! just fyi 
    # in the future, merge on Last Name
    mergedDF = pd.merge(peopleDF, transDF, on=['Full Name'], how='right',indicator=True)
    
    return mergedDF

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
    
def main(pathCA, pathBond, paths=None):
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
