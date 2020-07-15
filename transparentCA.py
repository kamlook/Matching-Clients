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

pathCities = r'D:\PPI Matching Names\Cities'
pathSpecDis = r'D:\PPI Matching Names\Special Districs'
pathCounties = r'D:\PPI Matching Names\Counties'
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
    nescJobs, jobsDF, filterTag = get_jobsDF(masterDF,paths)
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
    return masterDF, jobsDF, filterTag

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
            tempDF = pd.read_csv(dirName + "\\"  + fileList[-1], usecols = ['Employee Name','Job Title','Base Pay','Agency','Year']) 
            masterDF = pd.concat([masterDF,tempDF], ignore_index = True) # concatinate all files to one big data frame 
        else:pass
    return masterDF

def get_jobsDF(masterDF,paths=None):
    ### IDENTIFYING UNIQUE JOB TITLES AND ONLY KEEPING ONES USEFUL TO PPI ###
    jobTitles=masterDF['Job Title'].unique()
    necsJobs_list, filterTag = get_unique_jobs(paths) # beware, not as limiting as you may think. i.e analyst, manager
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
                
    # apply extras terms to blacklist depending on search conditions
    # SECTION TO GO THROUGH AND EDIT WITH KIMO
    if filterTag == 'planner':
        unnecsJobs_list = unnecsJobs_list + ['comm','aide','tech']
    elif filterTag == 'hr':
        unnecsJobs_list = unnecsJobs_list +[]
    elif filterTag == 'construction':
        unnecsJobs_list = unnecsJobs_list +[]
    elif filterTag == 'eng support':
        unnecsJobs_list = unnecsJobs_list +[]
    elif filterTag == 'engineer1':
        unnecsJobs_list = unnecsJobs_list + []
    else:
        pass          
                
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
    return nescJobs, jobsDF, filterTag

def get_unique_jobs(paths=None):
    uniqueJobs=[]
    xFilter_lol = [] # list of lists 
    # read through given bond files to find all bond jobs in the database
    options = ['1', 'planners', 'plan','2','hr','3','construction',
               '4', 'engineering support','5','engineering 1',
               '6','no extra filter','none','no']
    if paths == None:
        print('No path returned, using built-in system values')
        HR_jobs = ['Human Resources','HR','Hr','Personnel','Administ','Benefits Coordinator']
        filteredJobs = HR_jobs
        print('1: Planners')
        print('2: HR')
        print('3: Construction')
        print('4: Engineering Support')
        print('5: Engineering 1')
        print('6: No extra filter')
        extraFilter=input('Choose extra filter from selection above: ')
        while extraFilter not in options:
            extraFilter = input('Please choose from one of the 6 options listed above: ')
            
        # SECTION TO GO THROUGH AND EDIT WITH KIMO
        # defining nesc key terms for searches and tags allows for additional 
        #blacklists for specific search terms 
        if extraFilter in options[0:3]: #planner
            filteredJobs = ['Planner', 'Director of Buildings', 'Planning',
                            'Community Dev Director','Community Development',
                            'Director of Commmunity','Dir. Dev. Svcs','Manager of Water Resources',
                            'Compliance','Water Policy Manager']
            filterTag = 'planner'#director of community development 
        elif extraFilter in options[3:5]: #hr
            filteredJobs = ['Human Resources','HR','Hr','Personnel','Administ','Benefits Coordinator']
            filterTag = 'hr'
        elif extraFilter in options[5:7]: #construction
            filteredJobs = ['Construction', 'Field Engineering'] #take out building and inspector 
            filterTag = 'construction'
        elif extraFilter in options[7:9]: #engineering support
            filteredJobs = []
            filterTag = 'eng support'
        elif extraFilter in options[9:11]: #engineering 1
            filteredJobs = []
            filterTag = 'engineer1'
        elif extraFilter in options[11:-1]: #none
            filteredJobs = []
            filterTag = 'none'
            
    #path to explicit job csv provided         
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
        
    # output filtered jobs, if i need specific blacklists for each category, i may need to return
    # value that also indicates which black list to use 
    return filteredJobs, filterTag

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
    bondDF = pd.read_csv(pathBond, usecols = ['2 First_Name Alphanumeric','36 Nickname Alphanumeric',
                                              '37 Last Name Alphanumeric','41 Job Title Alphanumeric',
                                              '44 Employer Xref'])
    # change col names to be more easily readable and ready to merge with TransCA data
    bondDF = bondDF.rename(columns={'2 First_Name Alphanumeric': 'First Name',
                                    '36 Nickname Alphanumeric':'Nickname', '37 Last Name Alphanumeric':'Last Name',
                                    '41 Job Title Alphanumeric': 'Job Title Bond', '44 Employer Xref': 'Employer UniqueID'})
    # we need astype(str) to convert pd.Series object into a str
    #bondDF['Full Name'] = bondDF[['First Name', 'Last Name']].apply(lambda full: ' '.join(full.astype(str)),axis=1)
    
    return bondDF

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
    jobsDF['First Name']=firstName
    jobsDF['Middle Stuff']=middleIn
    jobsDF['Last Name']=lastName
    jobsDF['Extras']=extras
    
    return jobsDF

# peopleDF = bondDF
# transDF = jobsDF
def compare_dataframes(peopleDF, transDF):
    agencyPath = 'D:\PPI Matching Names\F02.csv'
    agencyDF = pd.read_csv(agencyPath, usecols = ['UniqueID','1 Company Alphanumeric'])
    agencyDF = agencyDF.rename(columns={'UniqueID':'Employer UniqueID'}) # change to match Bond people Data for merge
    
    #merge only valid if both first and last name match
    mergedDF = pd.merge(peopleDF, transDF, on=['First Name','Last Name'], how='outer',indicator='bondAndTrans') 
    comp_trans_only=mergedDF[mergedDF['bondAndTrans']=='right_only']
    comp_trans_only = comp_trans_only.drop(columns = ['Employer UniqueID'])
    comp_shared = mergedDF[mergedDF['bondAndTrans']=='both']
    #comp_shared.to_csv('TESTEST.csv',index=False)
    #agencyDF.to_csv('AgencyTestTest.csv', index=False)
    comp_shared = pd.merge(comp_shared, agencyDF, on = ['Employer UniqueID'], how = 'left', indicator=True)
    comp_shared = comp_shared.rename(columns={'1 Company Alphanumeric':'Bond Company'})
    return comp_trans_only, comp_shared

def confidence_matching(jobBond, jobTCA, companyBond, AgencyTCA): #is applied to every record in the comp_shared DataFrame
    '''
    INPUTS: 
        All inputs are elements of a Series and all should be of d-type=str
    '''
    # checking bond job and company data exists for the employee 
    if type(jobBond) != str:
        return 'Low - No Bond Job'
    if type(companyBond) != str:
        return 'Low - No  Bond Company Code Provided'
    
    # preppring data for checking if bond exists in TCA  
    jbTemp = jobBond.split()
    #jtcaTemp = jobTCA.split()    
    cbTemp = companyBond.split()
    #atcaTemp=AgencyTCA.split() 
    
    #Job match means automatic high confidence
    for jobSubStr in jbTemp:
        if jobSubStr in jobTCA:
            for compSubStr in cbTemp:
                if compSubStr in AgencyTCA:
                    return 'Very High' # City and Job Match
            return 'High' # Job match only 
    for compSubStr in cbTemp:
        if compSubStr in AgencyTCA:
            return 'Medium - City Match Only'
    return 'Low - No City or Job Match'   
              
def define_action(conLevel):
    if conLevel == 'Very High' or conLevel=='High':
        return 'Keep'
    elif conLevel == 'Medium - City Match Only':
        return 'Manual Check'
    else:
        return 'Leave'

def saving_csv(comp_trans_only, comp_shared, filterTag):
    # savingTCA = 'D:\PPI Matching Names\OnlyTransCAPeople\\' + filterTag + '.csv'
    pathShared = 'D:\PPI Matching Names\SharedPeople\\{}{}.csv'.format(filterTag,'Shared')
    comp_trans_only.to_csv('D:\PPI Matching Names\OnlyTransCAPeople\\{}{}.csv'.format(filterTag,'TransCA'),
                index=False)
    comp_shared.to_csv(pathShared, index=False)
    
    return pathShared

#now analyze the manually change csv
def manual_edits(pathShared,comp_trans_only):
    # make sure manual edits are properly made and saved
    notValidEdits = True
    while notValidEdits:
        confirm = input('Once all manual checks have been addressed save and close the file \nType and submit "Enter" to continue  ')
        if confirm.lower() == 'enter':
            notValidEdits = False
    editedDF = pd.read_csv(pathShared)
    #checking if all manual edit tags are gone 
    if 'Manual Check' in editedDF['Action'].unique(): # could be made more robust by only checking for leave and keep 
        print('Edit csv again, not all "Manual Checks" addressed')
        return manual_edits(pathShared,comp_trans_only)
    keepDF = editedDF[editedDF['Action']=='Keep']
    leaveDF = editedDF[editedDF['Action']=='Leave']
    comp_trans_only = pd.concat([comp_trans_only,leaveDF],ignore_index=True) # add unmatched employees back into search pool 
    
    return comp_trans_only
    
def main(pathCA, pathBond, paths=None):
    '''
    INPUTS
    str     pathCA: path to directory with Transparent California Files
    str     pathBond: path to Bond-People csv
    list    paths: list of paths bond files with unique job titles
    '''
            
    _, jobsDF, filterTag = parse_transparent_data(pathCA,paths)
    bondDF = parse_bond_data(pathBond)
    comp_trans_only, comp_shared = compare_dataframes(bondDF, jobsDF)
    comp_shared['Confidence Level'] = comp_shared.apply(lambda row: confidence_matching(row['Job Title Bond'], row['Job Title'],
                                                                                        row['Bond Company'], row['Agency']),axis=1)
    comp_shared['Action'] = comp_shared.apply(lambda row: define_action(row['Confidence Level']), axis=1)
    #only comment keeping beacuse kinda proud of the below line 
    #comp_shared['Action'] = comp_shared.apply(lambda row:'Keep' if row['Confidence Level'] =='Very High' or row['Confidence Level']=='High' else 'Leave', axis=1)
    pathShared = saving_csv(comp_trans_only, comp_shared, filterTag)
    comp_shared = manual_edits(pathShared,comp_shared)
    
    
    return comp_trans_only, comp_shared
