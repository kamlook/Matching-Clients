'''
Additional Cleaning after trans and bond comparison 
'''
import pandas as pd
from tkinter import filedialog
from tkinter import *
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
    # saving dataframes to be reviewed and edited by kimo or another person in the office
    if filterTag[-5:] == 'dupes':
        print('Dupes Case')
        comp_shared.to_csv('D:\PPI Matching Names\_DupesCheckFolder\{}.csv'.format(filterTag),
            index=False)
        comp_trans_only.to_csv('D:\PPI Matching Names\OnlyTransCAPeople\\{}{}.csv'.format(filterTag[:-5],'TransCA'),
            index=False)
        pathShared = 'Not needed with dupes'
    else:
        print(filterTag)
        region = input('What kind of area are you searching? \n[City, SpecDist, or County]  ')
        pathShared = 'D:\PPI Matching Names\SharedPeople\\{}{}{}.csv'.format(filterTag,region,'Shared')
        comp_shared.to_csv(pathShared, index=False)
    
    return pathShared

#now analyze the manually change csv
def manual_edits(pathShared,comp_trans_only):
    # make sure manual edits are properly made and saved
    notValidEdits = True
    while notValidEdits:
        confirm = input('\nOnce all manual checks have been addressed save and close the file \nType and submit "Enter" to continue  ')
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
    

    return comp_trans_only, keepDF

def dupes_chosen():
    root = Tk()
    pathCTO =  filedialog.askopenfilename(initialdir = "D:\PPI Matching Names",title = "Select cleaned TransCA csv",
        filetypes = (("csv files","*.csv"),("all files","*.*")))
    #pathCTO = askopenfilename(title='Select cleaned TransCA csv', initialdir='D:\PPI Matching Names',filetypes=("csv files","*.csv"))
    tempCTO = pd.read_csv(pathCTO)
    pathDupes =  filedialog.askopenfilename(initialdir = "D:\PPI Matching Names",title = "Select csv with CHOSEN duplicate employees",
        filetypes = (("csv files","*.csv"),("all files","*.*")))
    tempDupes = pd.read_csv(pathDupes)
    root.destroy()

    finalDF = pd.concat([tempCTO,tempDupes],ignore_index=True)
    filename=input('Desired file name (Will be saved to Final CSV Folder)   ')
    finalDF.to_csv('D:\PPI Matching Names\FinalCSV\{}FINAL.csv'.format(filename))

    return finalDF
