# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 14:43:10 2020

@author: Kam Look
"""
# script is used to identify all the unique jobs in given bond csv


import numpy as np
import pandas as pd

pathConstruct = r'D:\PPI Matching Names\PossibleJobs\construction.csv'
pathEng1 = r'D:\PPI Matching Names\PossibleJobs\engineer1.csv'
pathEngSupp = r'D:\PPI Matching Names\PossibleJobs\Engineering Support.csv'
pathPlanning = r'D:\PPI Matching Names\PossibleJobs\planning.csv'
pathHR = r'D:\PPI Matching Names\PossibleJobs\HR.csv'

paths = [pathConstruct, pathEng1, pathEngSupp, pathPlanning, pathHR]

def get_unique_jobs(paths):
    uniqueJobs=[]
    for file_path in paths:
        # print(file_path)
        temp_jobDF = pd.read_csv(file_path, usecols= ['JobTitle'], encoding="ISO-8859-1") # not utf-8 for some reason 
        tempUnique = temp_jobDF['JobTitle'].unique()
        uniqueJobs=uniqueJobs+ list(tempUnique) # add unique jobs to master list
    
    uniqueJobsClean = [x for x in uniqueJobs if str(x) != 'nan']
    
    return uniqueJobsClean



catergory = input('narrow down more? ')
print(catergory)
'''
dick = {'A': [1,2,3,4,], 'B': ['apple','watermelon','banana','kiwi']}
dick = pd.DataFrame(dick)
checklist = ['apple juice','banana','cat']
print(dick['B'].isin(checklist))
'''
#Cool Question festure but only works in the prompt window, not IDE 
'''
import inquirer
questions = [
  inquirer.List('size',
                message="What size do you need?",
                choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
            ),
]
answers = inquirer.prompt(questions)
print(answers["size"])
'''


oldList = ['Police', 'Fire', 'Pool', 'Intern', 'Park', 'Video' ,
                   'Graphics','Temp', 'Ztemp','Airport','Administrative A',
                   'Clerk', 'Administrato', 'Administrative Spec', 'Administrative Tech',
                   'Secretary', 'CUSTOMER', 'Attorney', 'Administrative C', 'Administrative H',
                   'Administrative Supp','Maintenance', 'Hrly', 
                   'Recreation','Library', 'Finance','Sport','Farm','Hous',
                   'Analyst', 'Aqua', 'Crime', 'Legis', 'Cement',
                   'Forensic', 'Custodian', 'Arts','Kids','Child', 'Peace', 'Homework',
                   'Battalion','Neighborhood','Ambulance', 'Emergency','Learning','Nutrition',
                   'Payroll', 'Coach', 'Public Sfty', 'Equip Oper', 'Cultur', 'Operator',
                   'Budget', 'Collector'] 

unnecsJobs_list=[]
for x in oldList:
    unnecsJobs_list.append(x.lower())
    