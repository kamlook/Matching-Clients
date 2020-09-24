# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 15:19:38 2020

@author: Kam Look
"""

from pyhunter import PyHunter
import pandas as pd

# newDf should be hunterInfo
def concat_to_master(email_list, newDF):
    # path = r'D:\PPI Matching Names\ENGfinalCSV.csv'
    # path = r'D:\PPI Matching Names\Planner_CityfinalCSV.csv'
    # path = r'D:\PPI Matching Names\HR_CityfinalCSV.csv'
    # path = r'D:\PPI Matching Names\Construct_CityfinalCSV.csv'
    path = r'D:\PPI Matching Names\ENG_county_finalCSV.csv'
    masterCSV = pd.read_csv(path)
    mergedDF = pd.merge(email_list, newDF, on=['Email'])
    updatedDF = pd.concat([masterCSV,mergedDF], ignore_index=True)
    updatedDF.to_csv(path, index=False)
    return print('Sucessfully updated {}'.format(path))

# Orange County emails: temp_list = email_list[834:954]['Email']
# SD County emails: temp_list = email_list[1091:1259]['Email']
# LA County Engineers: temp_list=email_list[400:]['Email']

hunter = PyHunter('c662e1e96cd2a1883640518bdd823013613c534b')
#verify=hunter.email_verifier('loconnell@anaheim.net')
categories = []
data = []
# NanData = ['noEmail']*12 + [[]]
# verify2 = hunter.email_verifier('LDavis@anaheim.net') # len=13
# To populate the dataframe we are just going to iterate through the dictionary
#   If sources are empty, then pass,else iterate through sources 
hunterInfo = pd.DataFrame(columns=['result','score', 'Email','regexp','gibberish',
                                   'disposable','webmail','mx_records','smtp_server',
                                   'smtp_check','accept_all','block','sources'])
total= len(temp_list)
counter = 0
for email in temp_list:
    counter += 1
    print('{}/{}'.format(counter,total))
    print('Verifying {}...'.format(email))
    verify_dict = hunter.email_verifier(email)    
    for items in verify_dict.items():
        # print(items)
        # print(type(items[0]))
        # categories.append(items[0])
        data.append(items[1])
    hunterInfo.loc[len(hunterInfo)] = data
    data = []


'''
for emails in email_list:
    verify_dict=email_verifier(emails)
    source = verify_dict['sources']
    if not source:
        'no source'
    else:
        'source exists'
        'flag and record source'
'''
    
   # finalCSV = pd.merge(email_list,hunterInfo, on=['Email'])
