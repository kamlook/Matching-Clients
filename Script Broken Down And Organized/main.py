# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 15:01:53 2020
@author: Kam Look
"""
import parseTrans
import bondAndComp
import postCompClean

# write paths for testing into easily testable variables

pathCities = r'D:\PPI Matching Names\Cities'
pathSpecDis = r'D:\PPI Matching Names\Special Districts'
pathCounties = r'D:\PPI Matching Names\Counties'
pathBond = r'D:\PPI Matching Names\BondAdaptPeople-Data.csv'

pathConstruct = r'D:\PPI Matching Names\PossibleJobs\construction.csv'
pathEng1 = r'D:\PPI Matching Names\PossibleJobs\engineer1.csv'
pathEngSupp = r'D:\PPI Matching Names\PossibleJobs\Engineering Support.csv'
pathPlanning = r'D:\PPI Matching Names\PossibleJobs\planning.csv'
pathHR = r'D:\PPI Matching Names\PossibleJobs\HR.csv'

paths = [pathPlanning, pathHR, pathConstruct, pathEngSupp, pathEng1] # will be iterated through    
    
    
    
def main(pathCA, pathBond, paths=None):
    '''
    INPUTS
    str     pathCA: path to directory with Transparent California Files
    str     pathBond: path to Bond-People csv
    list    paths: list of paths bond files with unique job titles
    '''
            
    _, jobsDF, filterTag = parseTrans.parse_transparent_data(pathCA,paths)
    bondDF = bondAndComp.parse_bond_data(pathBond)
    comp_trans_only, comp_shared = bondAndComp.compare_dataframes(bondDF, jobsDF)
    # assign confidence values to mathesbased on quality of matches
    comp_shared['Confidence Level'] = comp_shared.apply(lambda row: postCompClean.confidence_matching(row['Job Title Bond'], row['Job Title'],
                                                                                        row['Bond Company'], row['Agency']),axis=1)
    #Poor matches will be added back into TCA contact pool while strong maches removed
    comp_shared['Action'] = comp_shared.apply(lambda row: postCompClean.define_action(row['Confidence Level']), axis=1)
    #only comment keeping beacuse kinda proud of the below line 
        #comp_shared['Action'] = comp_shared.apply(lambda row:'Keep' if row['Confidence Level'] =='Very High' or row['Confidence Level']=='High' else 'Leave', axis=1)
    pathShared = postCompClean.saving_csv(comp_trans_only, comp_shared, filterTag)
    #pathShared = 'D:\PPI Matching Names\SharedPeople\hrSharedBACKUP.csv' # hr
    comp_trans_only, keepDF = postCompClean.manual_edits(pathShared,comp_trans_only) # if i can call this returning final, that would be nice
    dupes_to_be_checked = comp_trans_only[comp_trans_only.duplicated(['First Name','Last Name'],keep=False)]
    comp_trans_only = comp_trans_only.drop_duplicates(['First Name','Last Name'], keep=False)
    filterTag=filterTag+'dupes'
    pathDupes = postCompClean.saving_csv(comp_trans_only,dupes_to_be_checked,filterTag)
    
    return comp_trans_only, keepDF, dupes_to_be_checked

# after dupes are cleaned and selected, run finalDF=postCompClean.dupes_chosen()