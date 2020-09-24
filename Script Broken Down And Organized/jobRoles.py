'''
Job Role Creation
Based on Job title, populate Job role column with one of the following:
    ['{category} Executive', {category} Manager, {}category Supervisor, {category} Staff]
'''
import pandas as pd 

workingDF = pd.read_csv(r'C:\Users\Kam Look\Desktop\Kimo Files\UnmatchedPeople\ENG_county_Unmatched.csv')

def role_parsing(jobTitle, basePay, category):
    jobTitle = jobTitle.lower()
    basePay=float(basePay)
    print(basePay)
    execTitles = ['director', 'chief','city manager', 'drctr', 'general manager','dir',
                  'executive']
    mngrTitles = ['city traffic', 'manager', 'mgr']
    supVisTitles = ['project manager', 'principal', 'program manager', 'programs manager',
                    'projects manager', 'senior', 'planner iv', 'planner v',
                    'sr', 'head', 'superv','supv','sprvisor'] # earning 120k+ also makes you a supervisor 
    staffTitles = ['ass', 'official', 'eng', 'asoc', 'analyst', 'city planner', 'iii', 'ii',
                   'planner i', 'historic', 'tech','specialist','officer', 'off pt',
                   'coordinator','estimator','spec','inspect', 'wkr']

    if any(title in jobTitle for title in execTitles):
        return '{} Executive'.format(category)
    elif any(title in jobTitle for title in supVisTitles):
        return '{} Supervisor'.format(category)
    elif any(title in jobTitle for title in mngrTitles) or basePay >= 1.5e5:
        return '{} Manager'.format(category)
    elif 'eng' in jobTitle and basePay >= 1.2e5: # payCutoffs = {ENG: 1.2e5, HR: 1.1e5}
        return '{} Supervisor'.format(category)
    elif any(title in jobTitle for title in staffTitles) or jobTitle == 'planner':
        return '{} Staff'.format(category)
    else:
        return 'No confident match found! Improve parsing :('


    

def assign_role(workingDF):
    print('1: Planners')
    print('2: HR')
    print('3: Construction')
    print('4: Engineering Support')
    print('5: Engineering 1')
    print('Typing out whole title makes it easier')
    category =input('What kind of employees are these:   ') # adds more detail to job Role 
    workingDF['Job Role'] = workingDF.apply(lambda row: role_parsing(row['Job Title'], row['Base Pay'], category), axis=1)
    return workingDF