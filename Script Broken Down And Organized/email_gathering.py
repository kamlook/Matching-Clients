'''
After Final dfs are developed, this script reads those finals csvs and find email structures based on the agency

After list is developed, we will use Hunter.io to verify and check the confidence that these emails are legit.

'''

import pandas as pd
from tkinter import filedialog
from tkinter import *

# opening and reading to csvs we will ultimately compare 
def get_csv():
    root = Tk()
    pathFinal = filedialog.askopenfilename(initialdir = "D:\PPI Matching Names\OnlyTransCAPeople",title = "Select Final CSV",
        filetypes = (("csv files","*.csv"),("all files","*.*")))
    cleanedDF = pd.read_csv(pathFinal, usecols=['First Name','Last Name','Job Title','Base Pay','Year', 'Agency', 'Bond Company'])
    emailDF = pd.read_csv('D:\PPI Matching Names\OrganizationEmails.csv',
        usecols=['First Name','Last Name', 'Organization','work email'], encoding="ISO-8859-1")
    root.destroy()
    
    return emailDF, cleanedDF

def email_matching(agencyTCA, bondOrgList):
    # Current Problem, if agency string is small (san diego) gets picked up by wrong things in the list 
    # i.e caltrans - District 11- San Diego

    #Possible solution:
    # orgStrLen = 500 to start 
    # after finding a match, measure length of orgStr. if better match found with smaller length, replace orgStr
    # at the end 
    uselessOrgs = ['San Diego Grand Jury', 'Los Angeles County Regional Planning']
    orgStrLen = 500
    for org in bondOrgList:
        if org in uselessOrgs:
            pass
        else:
            if agencyTCA in org:
                if len(org) < orgStrLen:
                    validOrg = org
                    orgStrLen = len(org)
            elif agencyTCA == 'Los Angeles County Sanitation Districts':
                return 'County Sanitation District of Los Angeles County-Whittier'
            elif agencyTCA == 'San Bernardino Valley Municipal Water District':
                return 'City of San Bernardino Municipal Water Department'
            elif agencyTCA == 'Padre Dam Municipal Water District':
                return 'Padre Dam MWD'
            elif agencyTCA == 'Moulton-Niguel Water District':
                return 'Moulton Niguel Water District'
            elif agencyTCA == 'Ventura County':
                return 'Ventura County'

    if orgStrLen == 500:
        return 'No match in bond list'
    if orgStrLen < 500:
        return validOrg

# main function to get the proper email list

def city_email_matching(agencyTCA,listofCities):
    #matching for cities
    if agencyTCA == 'Vista':
        return 'City of Vista'
    for org in listofCities:
        if agencyTCA in org:
            return org
    return 'No match in Bond list'

def get_listofCities(bondOrgList):
    listofCities = []
    for org in bondOrgList:
        if 'City of' in org:
            listofCities.append(org)    
    return listofCities

def match_region():
    print('1: Cities')
    print('2: Special District')
    print('3: Counties')
    region=input('Choose region type you are matching [1, 2, or 3]: ')
    if region == '1': return 'cities'
    elif region == '2': return 'specdist'
    elif region == '3': return 'counties'
    else:
        print('must choose 1, 2, or 3')
        return match_region()

def get_domain_list():
    root = Tk()
    pathFinal = filedialog.askopenfilename(initialdir = "D:\PPI Matching Names",title = "Select OrganizationEmails CSV",
        filetypes = (("csv files","*.csv"),("all files","*.*")))
    domainDF = pd.read_csv(pathFinal, usecols=['Organization','work email'],encoding="ISO-8859-1")
    root.destroy()
    domain_col = domainDF['work email'].str.split('@', n=1, expand=True)
    '''
    domain_col.dropna(inplace=True)
    domain_list = list(domain_col[1].str.lower())
    uselessDomains = ['aol.com','gmail.com','cityofpasadena.net.','yahoo.com','projectpartners.com','Â']
    for domain in domain_list.copy():
        print('New Domain')
        for badName in uselessDomains:
            print(domain)
            if badName in domain:
                try:
                    domain_list.remove(domain)
                except ValueError:
                    pass
    domain_list=pd.Series(domain_list)
    domainDF['Domain'] = domain_list
    '''
    domainDF['Domain'] = domain_col[1].str.lower()
    # domainDF.dropna(inplace=True) # drop @nan domain
    domainDF.drop(['work email'], axis= 1, inplace=True) # inplace arg removes necessity for new variable creation. edits existing dataframe
    domainDF=domainDF[~domainDF.duplicated()]
    domainDF = domainDF.rename(columns={'Organization':'Email Agency'})

    return domainDF
# important NOTE: after looking through a majority of the city emails,I have come to the conclusion that a VAST majority of them follow the 'A' format 
# case A: {f}{last}@domain
def email_creation(cleanedDF, domainDF):
    newDF = pd.merge(cleanedDF,domainDF,on=['Email Agency'], how='left',indicator='emailMatches')
    newDF.dropna(subset=['Domain'], inplace = True)
    newDF['Email'] = newDF.apply(lambda row: address_building(row['First Name'],
     row['Last Name'], row['Domain']), axis=1)
    email_list = newDF[['First Name', 'Last Name', 'Job Title','Base Pay','Year', 'Agency', 'Email Agency', 'Email']]


    return email_list
# going to be used in a lambda .apply() function
def address_building(strFirstName, strLastName, strDomain):
    # for now we only do case A
    fInitial = strFirstName[0]
    strDomain=str(strDomain)
    if strDomain == 'ci.costa-mesa.ca.us':
        strDomain = 'costamesaca.gov'
    elif strDomain == 'ci.arcadia.ca.us':
        strDomain = 'arcadiaca.gov' 
    elif strDomain == 'ci.diamond-bar.ca.us':
        strDomain = 'diamondbarca.gov'
    elif strDomain == 'ci.el-monte.ca.us':
        strDomain = 'elmonteca.gov'
    elif strDomain == 'ci.encinitas.ca.us':
        strDomain = 'encinitasca.gov'
    elif strDomain == 'ci.laguna-hills.ca.us':
        strDomain = 'lagunahillsca.gov'
    elif strDomain == 'ci.newport-beach.ca.us':
        strDomain = 'newportbeachca.gov'
    elif strDomain == 'ci.ojai.ca.us':
        strDomain = 'ojaicity.org'
    elif strDomain == 'ci.ontario.ca.us':
        strDomain = 'ontarioca.gov'
    elif strDomain =='ci.palm-desert.ca.us':
        strDomain = 'cityofpalmdesert.org'
    elif strDomain == 'ci.poway.ca.us':
        strDomain = 'poway.org'
    elif strDomain == 'ci.rancho-mirage.ca.us':
        strDomain = 'ranchomirageca.gov'
    elif strDomain == 'sbcitywater.org':
        strDomain = 'sbmwd.org'
    elif strDomain == 'ci.san-dimas.ca.us':
        strDomain = 'sandimasca.gov'
    elif strDomain == 'wkrklaw.com':
        strDomain = 'smgov.net'
    elif strDomain == 'ci.san-marcos.ca.us':
        strDomain = 'san-marcos.net'
    elif strDomain == 'ci.south-pasadena.ca.us':
        strDomain = 'southpasadenaca.gov'
    elif strDomain == 'ci.pomona.ca.us':
        strDomain = 'pomona.ca.us'
    elif strDomain == 'ci.stanton.ca.us':
        strDomain = 'stanton.ca.us'
    elif strDomain == 'ci.ventura.ca.us':
        strDomain = 'cityofventura.net'
    elif strDomain == 'ci.vernon.ca.us':
        strDomain = 'cityofvernon.org'
    elif strDomain == 'ci.victorville.ca.us':
        strDomain = 'victorvilleca.gov'
    elif strDomain == 'ci.westminster.ca.gov':
        strDomain = 'westminer-ca.gov'
    elif strDomain == 'malibucity.org\t':
        strDomain = 'malibucity.org'
    elif strDomain == 'ci.azusa.ca.us':
        strDomain = 'azusaca.gov'
    elif strDomain == 'ci.brea.ca.us':
        strDomain = 'cityofbrea.net'
    elif strDomain == 'ci.camarillo.ca.us':
        strDomain = 'cityofcamarillo.org'
    elif strDomain == 'ci.chula-vista.ca.us':
        strDomain = 'chulavistaca.gov'
    elif strDomain == 'ci.colton.ca.us':
        strDomain = 'coltonca.gov'
    elif strDomain == 'ci.corona.ca.us':
        strDomain = 'coronaca.gov'
    elif strDomain == 'ci.glendale.ca.us':
        strDomain = 'glendaleca.gov'


    lInitial = strLastName[0]
    # removing nonalphanumeric charcters from people like "O'Donnell"
    alphanumeric_filter = filter(str.isalnum,strFirstName)
    strFirstName = ''.join(alphanumeric_filter)
    alphanumeric_filter = filter(str.isalnum,strLastName)
    strLastName = ''.join(alphanumeric_filter)    

    # caseA doamins will be default
    caseB_domains = ['cityofbrea.net','cityofbuellton.com', 'ci.commerce.ca.us', 'cityoffullerton.com','ci.garden-grove.ca.us',
                    'cityoflapalma.org','moval.org','rpv.com','rpvca.gov','ci.rolling-hills-estates.ca.us','fpud.com','mesawater.org',
                    'sbvmwd.com','smwd.com','westbasin.org','water.ca.gov','centralbasin.org']

    caseC_domains = ['calipatria.com','ci.lompoc.ca.us','ci.pomona.ca.us','pomona.ca.us']

    caseD_domains = ['carlsbadca.gov', 'coronaca.gov', 'culvercity.org', 'fountainvalley.org', 'hayward-ca.gov', 'longbeach.gov',
                    'lbwater.org', 'lacity.org', 'ladwp.com','cityofmaywood.org','oxnard.org','palmspringsca.gov','cityofrc.us',
                    'redondo.org','sbmwd.org','westcovina.org', 'ojaisan.org','ocpw.ocgov.com','ocwr.ocgov.com','sbcounty.gov',
                    'dpw.sbcounty.gov','ventura.org','cvwdwater.com','helixwater.org','polb.com','sdcounty.ca.gov','dot.ca.gov',
                    'ventura.org', 'ocpw.ocgov.com']

    caseE_domains = ['san-clemente.org','emwd.org','metro.net','ranchowater.com']
    caseF_domains = ['lomitacity.com']
    caseG_domains = ['sbcity.org']
    caseH_domains = ['walnut-creek.org','irwd.com']
    caseI_domains = ['rcsd.org', 'wqa.com','borregowd.org']
    caseJ_domains = ['vrsd.org']

    # check for big names like Los Angeles


    if any(strDomain == domain for domain in caseB_domains):
        # print('CaseB triggered')
        address = strFirstName + lInitial + '@' + strDomain
    elif any(strDomain == domain for domain in caseC_domains):
        address = fInitial + '_' +strLastName + '@' + strDomain
    elif any(strDomain == domain for domain in caseD_domains):
        # print('Case D triggered: ')
        address = strFirstName + '.' + strLastName + '@' + strDomain
    elif any(strDomain == domain for domain in caseE_domains):
        address = strLastName + fInitial +'@'+ strDomain
    elif any(strDomain == domain for domain in caseF_domains):
        address = fInitial + '_' + strLastName +'@' + strDomain
    elif any(strDomain == domain for domain in caseG_domains):
        address = strLastName + '_' + strFirstName[:2] +'@' + strDomain
    elif any(strDomain == domain for domain in caseH_domains):
        address = strLastName + "@" + strDomain
    elif any(strDomain == domain for domain in caseI_domains):
        address =  strFirstName + '@' + strDomain
    elif any(strDomain == domain for domain in caseJ_domains):
        address = strFirstName + strLastName + '@' +strDomain
    else:
        address = fInitial + strLastName +'@' + strDomain
    return address.lower()



#essentially the main of this script 
def get_email_list():
    emailDF, cleanedDF = get_csv()
    bondOrgList=list(emailDF['Organization'].unique())
    regionType = match_region()
    # domainDF =  get_domain_list()
    domainDF = pd.read_csv('D:\PPI Matching Names\DomainTableRefined.csv')
    if regionType == 'cities':
        listofCities = get_listofCities(bondOrgList)
        cleanedDF['Email Agency'] = cleanedDF.apply(lambda row: city_email_matching(row['Agency'],listofCities), axis=1)
    elif regionType == 'counties' or regionType == 'specdist':
        cleanedDF['Email Agency'] = cleanedDF.apply(lambda row: email_matching(row['Agency'],bondOrgList), axis=1)

    else:
        return print('Only testing cities right now')
    # cleanedDF['Email Agency'] = cleanedDF.apply(lambda row: email_matching(row['Agency'],bondOrgList), axis=1)
    cleanedDF.dropna(subset=['First Name'],inplace=True)
    email_list= email_creation(cleanedDF,domainDF)
    return email_list # ctrl + F testDF to remove 

def split_full_name(jobsDF):
    # make a series of List of the employees full names
    # drop NaN here, but show kimo the 5 or so entries at the end of bond data 
    # with no name
    jobsDF.dropna(subset=['1 Name Alphanumeric'], inplace=True)
    peopleSeries = jobsDF['1 Name Alphanumeric'].str.split(expand = False)
    suffix = ['jr','jr.','ii','iii']
    firstName = []
    lastName =[] # Last Yucca Valley people really threw the data for a loop. do them manually or just drop them? 
    middleIn = []
    extras = []
    tempSuffix =[]
    # making lists then adding the list to the dataframe straight away, no need to convert to series df['List']=list
    
    for nameList in peopleSeries:
        #jr and ending check
        print(nameList)
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
def address_split(bondNamesDF):
    addressSeries = bondNamesDF['18 Address1 Alphanumeric'].str.split(pat='~',n=1, expand=True)
    bondNamesDF['Home Address'] =addressSeries[0]
    bondNamesDF['Work Address'] =addressSeries[1]   
    return bondNamesDF





# cleanedDF.to_csv('July23rd_emailMatching.csv', index=False)