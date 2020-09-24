'''
parse bond data and compare matrices
'''
import pandas as pd
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

