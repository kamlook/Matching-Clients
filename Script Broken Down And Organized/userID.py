'''
Trying to parse cases to find userID formula
'''

import pandas as pd 


def finding_userID(firstName,lastName,workEmail):
    '''
    firstName: string
    lastName: string
    workEmail: string
    '''
    
    firstName=firstName.lower()
    lastName=lastName.lower()
    workEmail=workEmail.lower()
    emailParts=workEmail.split('@')
    userID =emailParts[0]
    # create cases to check userID
    caseA = firstName[0] + lastName
    caseB = firstName + lastName[0]
    caseC = firstName[0]+"_"+lastName
    caseD = firstName+'.'+lastName
    caseE = firstName
    caseF = lastName + firstName[0]
    # checking cases
    if userID == caseA:
        return 'A' 
    elif userID == caseB:
        return 'B' 
    elif userID==caseC:
        return 'C'
    elif userID==caseD:
        return 'D'
    elif userID==caseE:
        return 'E'
    elif userID == caseF:
        return 'F'
    else:
        print(userID)
        return 'No'
    
orgDF = pd.read_csv('D:\PPI Matching Names\OrganizationEmails.csv',
        usecols=['First Name','Last Name', 'Organization','work email'], encoding="ISO-8859-1")
orgDF.dropna(inplace=True)
orgDF['UserID formula'] = orgDF.apply(lambda row: finding_userID(row['First Name'],row['Last Name'], row['work email']),axis=1)

# after the emails are sorted, input all non-A types into email_gathering.py manually 


