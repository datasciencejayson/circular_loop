# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:59:27 2018

@author: Jayson Backes
"""

import os


def findText(inList, fileType, searchTerm):
    """
    This function takes a directory or a list of directories and searches all folders
    for a type of file using set of text that the user defines
    """
    if type(inList) == str:
        newList = inList.split()
    else:
        newList = inList
    import os
    #    for item in newList:
    #        print(item)
    #        if "\\" in item:
    #            if item[0].lower() != 'r'
    #            item = item.replace("\\","/")

    from os import listdir
    from os.path import isfile, join
    outList = []
    return outList


    for ivalue, i in enumerate(newList):
        print(i)
        for root, dirs, files in os.walk("/data2/users/jbackes/personal_env/prophet/env"):
            # print(root, dirs)
            for file in files:
                # if file.endswith('.py'):
                    # print(file)
                try:
                    with open(os.path.join(root, file), 'r') as text:
                        data = text.read()
                        if 'Python 3.7.4 64-bit (conda)' in data:
                            print(os.path,'---', root, file, '----------------------------')
                    text.close()
                except:
                    None



                        print(file - data)
            outList.append(os.path.join(root, file))
            text.close()
                print(root, dirs)



    
            #            print(root, dirs, files)
            for file in files:
                if file.endswith(fileType):
                    if fileType == '.sas':
                        with open(os.path.join(root, file), 'r', encoding='latin1') as text:
                            data = text.read()
                            if searchTerm in data:
                                outList.append(os.path.join(root, file))
                                text.close()
                            else:
                                text.close()
                    else:
                        with open(os.path.join(root, file), 'r') as text:
                            data = text.read()
                            if searchTerm.lower() in data.lower():
                                outList.append(os.path.join(root, file))
                                text.close()
                            else:
                                text.close()
    return outList


fileList = findText(["P:/", "Y:/jbackes", "Z:/", "G:/jbackes"],
                    ".sas",
                    "%substr")

#fileList = findText(["P:/"],
#                    ".py",
#                    "0 == 0")

#for i in fileList:
 #   print(i)

#inList = ["Z:\Analytics_Projects\030_IBP_Forecasting_Model_2015\a_raw_data"]
#
#j = "JAY$0N"


def charReplace(inputVar,
                chars="""~`!@#$%^&*()[]{}_+-=/\|"':;?<>.,""",
                repace_char=' '):
    if type(inputVar) == str:
        for c in chars:
            inputVar = inputVar.replace(c, " ")
        return inputVar
    if type(inputVar) == list:
        print('list')
        outputVar = []
        for string in inputVar:
            print(string)
            for c in chars:
                string = string.replace(c, " ")
            outputVar.append(string)
        return outputVar


charReplace(j, 'j', '_')

for root in os.walk("P:/"):
    print(root)
inList = ["Z:\Common", "Z:\Analytics"]
fileType = '.sas'
searchTerm = "searchTerm"
["C:/Users/backesj", "H:/", "S:/DA_work_files/DA_work_jayson"]



--------------------------------------------------------------


from datetime import date, timedelta
from dateutil.relativedelta import *
import datetime
import pandas as pd

date_override = '01jan2021'
current_date = datetime.datetime.strptime(date_override, "%d%b%Y").date() - relativedelta(months=1)
mid_date = datetime.datetime.strptime(date_override, "%d%b%Y").date() - relativedelta(months=2)
lookup_date = datetime.datetime.strptime(date_override, "%d%b%Y").date() - relativedelta(months=3)
print(current_date)

current_date = current_date.strftime("%Y%m")
mid_date = mid_date.strftime("%Y%m")
lookup_date = lookup_date.strftime("%Y%m")
print(d1)





file_list = [file for file in os.listdir(temp_folder) if 'event' not in file 
				and 'headcount' not in file
				and 'final_curves' not in file
				and 'bcat' not in file
				and '.db' not in file]

print(len(file_list) , file_list)




reference_date = datetime.date.today() 
reference_date = datetime.date(2020,5,5)

run_name = '05may2020'

idx = (reference_date.weekday() + 1) % 7

forecast_start = reference_date - datetime.timedelta(idx)


min_begin_date_week = forecast_start - datetime.timedelta(weeks=157)
min_begin_date_day = forecast_start - datetime.timedelta(weeks=105)
print(forecast_start, '-', min_begin_date_week, '-', min_begin_date_day)






import pandas as pd

df_full = pd.read_sas("/data2/bsro/00028_ld_mvp1/data/temp/forecast_only.sas7bdat", encoding='latin1')

df_full.head()

import seaborn as sns

import matplotlib.pyplot as plt
sns.set(style="ticks", color_codes=True)


sns.catplot(x='DAY_OF_WEEK', y='PREDICT', data=df)

sns.boxplot(x='DAY_OF_WEEK', y='PREDICT', data=df)


sns.distplot(x='DAY_OF_WEEK', y='PREDICT')

sns.catplot(x='DAY_OF_WEEK', y='PREDICT',
            kind="violin", data=df)


df = df_full[df_full["STORE_ID"]=='000027']
df.head()
list_days = "null,Sun,Mon,Tue,Wed,Thu,Fri,Sat".split(',')
for i in range(1,7):
    plt.figure()
    temp_df = df[df['DAY_OF_WEEK'] == i]
#    df.groupby("DAY_OF_WEEK").describe(percentiles=[.91])
    sns.distplot(temp_df['PREDICT']).set_title("{} - percentile = {}".format(list_days[i], temp_df.quantile(.9)))
    plt.figure()
    ax = sns.boxplot(x=temp_df['PREDICT'], whis=[5, 90]).set_title("{}".format(list_days[i]))
    plt.grid(True)
    plt.figure()
    ax = sns.boxenplot(x='DAY_OF_WEEK', y='PREDICT', data=df).set_title("{}".format(list_days[i]))
    ax = sns.stripplot(x='DAY_OF_WEEK', y='PREDICT', data=df,
                    size=4, color="gray").set_title("{}".format(list_days[i]))



ax = sns.boxenplot(x='DAY_OF_WEEK', y='PREDICT', data=df)
ax = sns.stripplot(x='DAY_OF_WEEK', y='PREDICT', data=df,
                   size=4, color="gray")








def ensure_path(input_path):
    list_path = []
    import os
    if os.path.exists(input_path) == True:
        new_path = input_path
        return new_path
    if os.path.exists(input_path) == False:
        for i, ivalue in enumerate(input_path.split('/')):
            if ivalue != '':
                if ivalue in ('Z:','Y:'):
                    list_path.append('//data2')
                elif ivalue in ('sas1'):
                    list_path.append('/')
                else:
                    list_path.append(ivalue)
            new_path = "/".join(list_path)
        print(new_path)
        if os.path.exists(new_path) == True:
            return new_path
        else:
            print('File Path Does not Exist')
            return 'NONE'

import pandas















# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 14:34:05 2018

@author: BackesJayson
"""
import os
import pandas as pd
import os

from os import listdir
from os.path import isfile, join

file_name = input("Please type the name of the")

DIR = "P:/Tools"

file_types = ".xlsx, .xls, .xls, .xlsm, .xlsb, .csv, .txt".replace(' ', '').split(",")

file_type = "xlsx"

file_name = "exxcel"

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def checkDIR(DIR):
    """
    this checks to see if the Directory exists

    """
    try:
        listdir(DIR)
    except FileNotFoundError:
        print("path does not exist")


checkDIR(DIR)


def getLatestFile(DIR, FileType):
    # import os packages

    # import platform
    try:
        file_list = [f for f in listdir(DIR) if isfile(join(DIR, f)) and file_name in f.lower()]
    except NameError:
        print("file not found")

    # create file list of xls files in download file directory
    file_list2 = []
    for file in file_list:
        # get date of file creation in download file directory
        file_list2.append(os.path.getmtime('%s/%s' % (DIR, file)))
    # create empty dictionary
    d = {}
    # create dictionary of files and date
    for i in range(len(file_list)):
        d[file_list[i]] = file_list2[i]

    # get max item in dictionary (last item created) this should be the file you
    # downloaded from the website
    import operator
    return d


#    return max(d.items(), key=operator.itemgetter(1))[0]


max_value = getLatestFile('P:/Tools', '.xlsx')

df = pd.read_csv("{0}/{1}.{2}".format(in_location, file_name, file_type),
                 index_col=None, skiprows=None, nrows=None, doublequote=True,
                 delimiter=None

                 )

xl = pd.ExcelFile("{0}/{1}.{2}".format(in_location, file_name, file_type))

names = xl.sheet_names

df = pd.read_excel("{0}/{1}.{2}".format(in_location, file_name, file_type))

xl.parse(sheet_name)

# Positional arguments
# are placed in order
print("{0} love {1}!!".format("GeeksforGeeks",
                              "Geeks"))

# Reverse the index numbers with the
# parameters of the placeholders
print("{1} love {0}!!".format("GeeksforGeeks",
                              "Geeks"))

"""
pandas.read_csv(filepath_or_buffer, sep=', ', delimiter=None, header='infer', 
                names=None, index_col=None, usecols=None, squeeze=False, 
                prefix=None, mangle_dupe_cols=True, dtype=None, engine=None, 
                converters=None, true_values=None, false_values=None, 
                skipinitialspace=False, skiprows=None, nrows=None, 
                na_values=None, keep_default_na=True, na_filter=True, 
                verbose=False, skip_blank_lines=True, parse_dates=False, 
                infer_datetime_format=False, keep_date_col=False,
                date_parser=None, dayfirst=False, iterator=False,
                chunksize=None, compression='infer', thousands=None,
                decimal=b'.', lineterminator=None, quotechar='"', quoting=0, 
                escapechar=None, comment=None, encoding=None, dialect=None, 
                tupleize_cols=None, error_bad_lines=True, warn_bad_lines=True, 
                skipfooter=0, doublequote=True, delim_whitespace=False,
                low_memory=True, memory_map=False, 
                float_precision=None)
"""





# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 14:42:07 2020

@author: BackesJayson
"""

import os
from random import randint
from time import sleep
def beep_boop():
    for i in range(20):
        if i == 0:
            print('beep!')
            os.system(r"start C:\Users\backesjayson\Downloads\beep_boop\mp3\beep.mp3")
        rand = randint(1, 2)
        if rand == 1:
            print('beep!')
            os.system(r"start C:\Users\backesjayson\Downloads\beep_boop\mp3\beep.mp3")
        else:
            print('boop!')
            os.system(r"start C:\Users\backesjayson\Downloads\beep_boop\mp3\beep1.mp3")
            
    print("""
                                _.-------.
                      |\---/|  / )  Cat  |
          ------------;     |-/ /| Food! |---
                      )     (' / `-------'
          ===========(       ,'==========
          ||   _     |      |
          || o/ )    |      | o
          || ( (    /       ;              (George)
          ||  \ `._/       /
          ||   `._        /|
          ||      |\    _/||
        __||_____.' )  |__||____________
         ________\  |  |_________________
                  \ \  `-.
                   `-`---'  
             
                            _,'|             _.-''``-...___..--';)
                           /_ \'.      __..-' ,      ,--...--'''
        (Kimchi)          <\    .`--'''       `     /'
                           `-';'               ;   ; ;
                     __...--''     ___...--_..'  .;.'
                    (,__....----'''       (,..--''
                   and (Kirra)
            
                   .-o=o-.
               ,  /=o=o=o=\ .--.
              _|\|=o=O=o=O=|    |
          __.'  a`\=o=o=o=(`\   /
          '.   a 4/`|.-""'`\ \ ;'`)   .---.
            \   .'  /   .--'  |_.'   / .-._)
             `)  _.'   /     /`-.__.' /
              `'-.____;     /'-.___.-'
                       `"'`
             """)
          
    input('You have just been Catsnowed! ')
beep_boop()


# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 19:42:44 2020

@author: BackesJayson
"""
import pandas as pd
mypath = "P:/gdi"
from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for i in onlyfiles:
    df = pd.read_sas("{}/{}".format(mypath,i), encoding = 'latin')
    df.to_csv("{}/{}.csv".format("G:/jbackes/gdi",i[0:i.find('.')]),index=False)









# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from itertools import permutations 
  
# Get all permutations of [1, 2, 3] 
perm = permutations([0,1,2,3,4,5,6]) 
  
# Print the obtained permutations 
tup_list = []
for i in list(perm): 
    if sum(i[0:3]) == 6:
        tup_list.append(i[0:3])
        
        
import os
import glob
import pandas as pd
os.chdir(r"g:/jbackes/oil")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "Oil_All.csv", index=False, encoding='utf-8-sig')


mean = 0
std = 1
j = 10



def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

for i in frange(-3,3+6/j,6/j):
    print(i)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:23:59 2020

@author: BackesJayson
"""

import geopandas
import geopy
import geocoder
import pandas as pd

df = pd.read_csv("G:/jbackes/tools/geocode/store_geocode.csv")

df = df[df.index <20]
df['full'] = df['ADDRESS_LINE_1']+" "+df['CITY']+" "+df['STATE_CODE']+" "+df['ZIP_CODE'].astype(str)
address_list = list(df['full'])
store_list = list(df['STORE_ID'])
from time import sleep
confidence_list = []
lat_list = []
lon_list = []
all_info_list = []
new_store_list = []
for i, ivalue in enumerate(address_list):
    sleep(1)
    g = geocoder.tomtom(ivalue, key='mqd9Sky490AjkjMfgnMtUMeiT4HSfFwE')
    print(g)
    new_store_list.append(store_list[i])
    confidence_list.append(g.json['confidence'])
    lat_list.append(g.json['lat'])
    lon_list.append(g.json['lng'])
    all_info_list.append(g.json)
    
    
df_new = pd.DataFrame(list(zip(confidence_list, lat_list, lon_list, new_store_list)), 
                     columns = 'confidence,lat,lon,store'.split(','))  

  
g.text()
import json
v = json.loads(g)
g.json['score']
v = g.json



from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="store_locator")
print(address_list[0])
location = geolocator.geocode("1116 Mill Creek Road")
location = geolocator.geocode("2320 dennywood dr")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)

d

locator = Nominatim(user_agent="myGeocoder")
from geopy.extra.rate_limiter import RateLimiter

# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
# 2- - create location column
df['new'] ="Karlaplan 13,115 20,STOCKHOLM,Stockholms län, Sweden"
df['location'] = df['new'].apply(geocode)
# 3 - create longitude, laatitude and altitude from location column (returns tuple)
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
# 4 - split point column into latitude, longitude and altitude columns
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)





locator = Nominatim(user_agent='myGeocoder')
import requests

response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA')

resp_json_payload = response.json()

print(resp_json_payload['results'][0]['geometry']['location'])

from  geopy.geocoders import Nominatim
geolocator = Nominatim()
city ="London"
country ="Uk"
loc = geolocator.geocode(city+','+ country)
print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)

   
import requests

GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

params = {
'address': 'oshiwara industerial center goregaon west mumbai',
'sensor': 'false',
'region': 'india'
}

# Do the request and get the response data
req = requests.get(GOOGLE_MAPS_API_URL, params=params)
res = req.json()

# Use the first result
result = res['results'][0]

geodata = dict()
geodata['lat'] = result['geometry']['location']['lat']
geodata['lng'] = result['geometry']['location']['lng']
geodata['address'] = result['formatted_address']

print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))





# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 14:59:27 2018

@author: Jayson Backes
"""

import os


def findText(inList, fileType, searchTerm):
    """
    This function takes a directory or a list of directories and searches all folders
    for a type of file using set of text that the user defines
    """
    if type(inList) == str:
        newList = inList.split()
    else:
        newList = inList
    import os
    #    for item in newList:
    #        print(item)
    #        if "\\" in item:
    #            if item[0].lower() != 'r'
    #            item = item.replace("\\","/")

    from os import listdir
    from os.path import isfile, join
    outList = []
    for ivalue, i in enumerate(newList):
        print(i)
        for root, dirs, files in os.walk(i):
            if ivalue % 200 == 0:
                print(root, dirs)
            #            print(root, dirs, files)
            for file in files:
                if file.endswith(fileType):
                    if fileType == '.sas':
                        with open(os.path.join(root, file), 'r', encoding='latin1') as text:
                            data = text.read()
                            if searchTerm in data:
                                outList.append(os.path.join(root, file))
                                text.close()
                            else:
                                text.close()
                    else:
                        with open(os.path.join(root, file), 'r') as text:
                            data = text.read()
                            if searchTerm.lower() in data.lower():
                                outList.append(os.path.join(root, file))
                                text.close()
                            else:
                                text.close()
    return outList


fileList = findText(["P:/", "Y:/jbackes", "Z:/", "G:/jbackes"],
                    ".sas",
                    "%substr")

#fileList = findText(["P:/"],
#                    ".py",
#                    "0 == 0")

#for i in fileList:
 #   print(i)

#inList = ["Z:\Analytics_Projects\030_IBP_Forecasting_Model_2015\a_raw_data"]
#
#j = "JAY$0N"


def charReplace(inputVar,
                chars="""~`!@#$%^&*()[]{}_+-=/\|"':;?<>.,""",
                repace_char=' '):
    if type(inputVar) == str:
        for c in chars:
            inputVar = inputVar.replace(c, " ")
        return inputVar
    if type(inputVar) == list:
        print('list')
        outputVar = []
        for string in inputVar:
            print(string)
            for c in chars:
                string = string.replace(c, " ")
            outputVar.append(string)
        return outputVar


charReplace(j, 'j', '_')

for root in os.walk("P:/"):
    print(root)
inList = ["Z:\Common", "Z:\Analytics"]
fileType = '.sas'
searchTerm = "searchTerm"
["C:/Users/backesj", "H:/", "S:/DA_work_files/DA_work_jayson"]









# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:23:59 2020

@author: BackesJayson
"""

import geopandas
import geopy
import geocoder
import pandas as pd


import paramiko
import getpass

# name the SSHClient
ssh = paramiko.SSHClient()

# set missing host policy
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# set the target_host address
target_host = 'appdsa01pakr'

# start the connection
ssh.connect( hostname = target_host, username = 'backesjayson@bfusa.com', \
            password = getpass.getpass("SAS Password: "))


stdin, stdout, stderr = ssh.exec_command("python /data2/Common/jbackes/tools/geocode/store_attribute_pull.py")

#unpickle geocoded df
unpickled_df = pd.read_pickle("G:/jbackes/tools/geocode/geocoded.pkl")
unpickled_df_nan = unpickled_df[unpickled_df['tomtom_country'].isnull() ]
captured_list = list(unpickled_df['STORE_ID'])
captured_nan = list(unpickled_df_nan['STORE_ID'])
df = pd.read_csv("G:/jbackes/tools/geocode/store_attributes.csv")


df = df[~df['STORE_ID'].isin(captured_list) | df['STORE_ID'].isin(captured_nan)]



df['full'] = df['ADDRESS_LINE_1']+" "+df['CITY']+" "+df['STATE_CODE']+" "+df['ZIP_CODE'].astype(str)
df.head()
address_list = list(df['full'])
store_list = list(df['STORE_ID'])

from time import sleep
confidence_list = []
lat_list = []
lon_list = []
all_info_list = []
new_store_list = []
capture_dict = {}
all_info_dict = {}
error_list = []
for i, ivalue in enumerate(address_list):
    print(ivalue)
    sleep(1)
    g = geocoder.tomtom(ivalue, key='mqd9Sky490AjkjMfgnMtUMeiT4HSfFwE')
    # capture_dict[ivalue] = g.json
    # new_store_list.append(store_list[i])
    # confidence_list.append(g.json['confidence'])
    # lat_list.append(g.json['lat'])
    # lon_list.append(g.json['lng'])
    # all_info_list.append(g.json)
    if g.json == None:
        print('none')
        error_list.append(store_list[i])
        all_info_dict[store_list[i]] = {'address':'ERROR'}
    else:
        all_info_dict[store_list[i]] = g.json

# df_lat_lon = pd.DataFrame(list(zip(confidence_list, lat_list, lon_list, new_store_list)), 
#                      columns = 'confidence,lat,lon,STORE_ID'.split(','))  
df_dict = pd.DataFrame.from_dict(all_info_dict, orient='index')
df_dict = df_dict.add_prefix('tomtom_')
df_dict['STORE_ID'] = df_dict.index
df_final = pd.merge(df, df_dict, how='left', on = ['STORE_ID', 'STORE_ID'])

df_appended = unpickled_df.append(df_final, sort=True)
# df_appended.drop(['confidence','lat','lon'], axis = 'columns', inplace=True)
#pickle it

df_appended.to_csv("G:/jbackes/tools/geocode/geocoded_stores.csv")
df_appended.to_pickle("G:/jbackes/tools/geocode/geocoded.pkl")


#compare results



















    
error_list = []
for k, v in dict(all_info_dict).items():
    if v is None:
        error_list.append(all_info_dict[k])
        del all_info_dict[k]


        
        
df_temp = pd.merge(df, df_new, how='left', on = ['STORE_ID', 'STORE_ID'])




df_index['lat_diff'] = df_index.LATITUDE-df_index.lat
df_index['lon_diff'] = df_index.LONGITUE-df_index.lon


frames = [df,df_new]

df_keys = pd.concat(frames, keys=['STORE_ID', 'store'])

g.text()
import json
v = json.loads(g)
g.json['score']
v = g.json



from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="store_locator")
print(address_list[0])
location = geolocator.geocode("1116 Mill Creek Road")
location = geolocator.geocode("2320 dennywood dr")
print(location.address)
print((location.latitude, location.longitude))
print(location.raw)

d

locator = Nominatim(user_agent="myGeocoder")
from geopy.extra.rate_limiter import RateLimiter

# 1 - conveneint function to delay between geocoding calls
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)
# 2- - create location column
df['new'] ="Karlaplan 13,115 20,STOCKHOLM,Stockholms län, Sweden"
df['location'] = df['new'].apply(geocode)
# 3 - create longitude, laatitude and altitude from location column (returns tuple)
df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else None)
# 4 - split point column into latitude, longitude and altitude columns
df[['latitude', 'longitude', 'altitude']] = pd.DataFrame(df['point'].tolist(), index=df.index)





locator = Nominatim(user_agent='myGeocoder')
import requests

response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=1600+Amphitheatre+Parkway,+Mountain+View,+CA')

resp_json_payload = response.json()

print(resp_json_payload['results'][0]['geometry']['location'])

from  geopy.geocoders import Nominatim
geolocator = Nominatim()
city ="London"
country ="Uk"
loc = geolocator.geocode(city+','+ country)
print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)

   
import requests

GOOGLE_MAPS_API_URL = 'http://maps.googleapis.com/maps/api/geocode/json'

params = {
'address': 'oshiwara industerial center goregaon west mumbai',
'sensor': 'false',
'region': 'india'
}

# Do the request and get the response data
req = requests.get(GOOGLE_MAPS_API_URL, params=params)
res = req.json()

# Use the first result
result = res['results'][0]

geodata = dict()
geodata['lat'] = result['geometry']['location']['lat']
geodata['lng'] = result['geometry']['location']['lng']
geodata['address'] = result['formatted_address']

print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))







































