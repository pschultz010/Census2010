import pandas as pd
import requests as requests
import time

# Build base URL
HOST = "https://api.census.gov/data"
year = "2010"
dataset = "dec/sf1"
base_url = "/".join([HOST, year, dataset])

# Get state & state code
predicates = {}
predicates['get'] = 'NAME'
predicates['for'] = 'state:*'
predicates['key'] = '756fedd78401f5418aa94263f18cf185329ea90a'
r = requests.get(base_url, params=predicates)

# Get population of ages by sex and race
races = {'A': 'white',
         'B': 'black',
         'C': 'american indian or alaska native',
         'D': 'asian',
         'E': 'native hawaiian or other pacific islander',
         'F': 'other',
         'G': 'two or more',
         'H': 'hispanic'}

for k, v in races.items():
    # race_sex_age : DataFrame for particular race
    # Get state & state code
    predicates = {}
    predicates['get'] = 'NAME'
    predicates['for'] = 'state:*'
    predicates['key'] = '756fedd78401f5418aa94263f18cf185329ea90a'
    r = requests.get(base_url, params=predicates)
    race_sex_age = pd.DataFrame(columns = ['state', 'state code'], data = r.json()[1:])

    column = ''
    sex = 'male'
    age = -2
    for i in range(1, 210):
        # build key for api call    (starting key: PCT012A001)
        predicates['get'] = 'PCT012' +k +'{0:0=3d}'.format(i)
        r = requests.get(base_url, params=predicates)

        # build column title
        if i == 1:
            column = 'total'
        elif i == 2 or i == 106:
            if i == 106:
                sex = 'female'
                age = -1
            column = sex
        elif i == 3 or i == 107:
            column = '{} under {}'.format(sex, age+1)
        elif i == 103 or i == 207:
            column = '{} {}'.format(sex, '100-104')
        elif i == 104 or i == 208:
            column = '{} {}'.format(sex, '105-109')
        elif i == 105 or i == 209:
            column = '{} {}'.format(sex, '110+')
        else:
            column = '{} {}'.format(sex, age)
        age += 1
        print(column)
        # add column to dataframe
        race_sex_age[column] = [item[0] for item in r.json()[1:]]
    race_sex_age.to_csv('/Users/Peter/Projects/Census/{}_sex_age.csv'.format(v.replace(" ", "_")))