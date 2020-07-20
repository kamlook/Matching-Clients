# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 12:21:26 2020

@author: Kam Look
"""

# new file to test ideas in DELETE LATER, its no big deal 
'''
words = ['director','manager', 'division','division manager Engineer plan',
         'waste water director', 'water manager', 'transportation manager',
         'community development manager']
matching = ['manager', 'division', 'director']
or_words = ['utilities','utility','water', 'community ']


for job in words:
    if all(x in job for x in matching):
        print('yay')
    elif any(x in job for x in or_words) and any(x in job for x in matching):
        print('yay2')
    elif 'transportation' in job and any(x in job for x in matching):
        print('yay3')
    elif 'community dev' in job and any(x in job for x in matching):
        print('yay4')
    else:
        print('sad')
'''

def eng_parsing(jobTitles):
    print('Engineering Parsing Chosen')
    nescJobs = [] # clear old nescJobs from other choices 
    # finding high level managment officials in all relevant departments
    department = ['Division','Utilities','Utility','Water','Building', 
                  'Building And Safety','Building & Safety', 'Transportation', 
                  'Solid Waste', 'Community Dev', 'Community Ser', 'Project',
                  'Program'] 
    mgmtRole = ['Director','Manager','Head','Chief','Supervisor','Official']
    # Compares every relevant department to every desired managment position
    for jobs in jobTitles:
        if any(x in jobs for x in department) and any(x in jobs for x in mgmtRole):
            nescJobs.append(jobs)
        elif 'Capital Project' in jobs or 'CIP' in jobs:
            nescJobs.append(jobs)
        elif 'General Man' in jobs or 'GM' in jobs:
            nescJobs.append(jobs)
    return nescJobs

        
        
    
    