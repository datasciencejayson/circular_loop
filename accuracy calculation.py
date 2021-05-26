# Check the accuracy


import os
import shutil
import pandas as pd
from datetime import datetime, date, timedelta
import pickle

# options

# pickle final dict for working use

pickling_on = 'Y'

# set important parameters
time_delta = 300
current_month = (date.today()-timedelta(days=4)).month
current_month
current_year = (date.today()-timedelta(days=4)).year
current_year

# current_month = (date.today()-timedelta(days=20)).month
print(current_month)
# source and destination for archiving old outputs

source = "/data2/bsro/00028_ld_mvp1/output"
destination = "/data2/bsro/00028_ld_mvp1/output/archive"
outpath = "/data2/bsro/00028_ld_mvp1/output/accuracy_reports"


# Step 1, Archive old forecasts


file_list = [file for file in os.listdir(source) if 'run' in file or 'valid' in file]

print(len(file_list) , file_list)

date_list = [item[0:9] for item in file_list]
print(date_list)

archive_list = []
for i, ivalue in enumerate(date_list):
    if date.today() - datetime.strptime(ivalue, '%d%b%Y').date() > timedelta(days=365):
        archive_list.append(file_list[i])

print(archive_list)


for i, ivalue in enumerate(archive_list):
    print(f'Moving {ivalue} from {source} to {destination}')
    dest = shutil.move("{}/{}".format(source,archive_list[i]),
                "{}/{}".format(destination,archive_list[i]))


# Set up useful functions

def pickle_your_object(pickle_object, file_name):
    pickle.dump(pickle_object, open('{}/pickle_files/{}.pickle'.format(source,file_name), 'wb'))
    print('{} has been pickled'.format(file_name))

def unpickle_your_object(file_name):
    try:
        pickle_object = pickle.load(open('{}/pickle_files/{}.pickle'.format(source,file_name), 'rb'))
        print('{} _has_ been unpickled'.format(file_name))
        return pickle_object
    except:
        print('{} _has not_ been unpickled. An empty dictionary was been created'.format(file_name))
        file_name = {}
        return file_name


# get max file

date_list = [item[0:9] for item in file_list]
print(date_list)



for i, ivalue in enumerate(date_list):
    if i == 0:
        max_value = datetime.strptime('01JAN2015', '%d%b%Y').date()
    temp_date = datetime.strptime(ivalue, '%d%b%Y').date()

    if temp_date >= max_value:
        max_value = temp_date
        max_date = ivalue
        print(max_date)




# Do CST first ;

#read back in pickle file to save itteration time

headcount_accuracy_df_dict_cst = unpickle_your_object("headcount_accuracy_df_dict_cst")

#headcount_accuracy_df_dict_cst = {}
#df_dict_cst = {}
#df_dict_daily_cst = {}
#df_dict_weekly_cst = {}
#df_list_weekly_cst = []
#df_list_daily_cst = []
time_list = 'daily,weekly'.split(',')
for i, ivalue in enumerate(time_list):
    file_list2 = [file for file in os.listdir(source) if 'run' in file and 'cst' in file and ivalue in file]
    print(file_list2)
    for j, jvalue in enumerate(file_list2):
        if jvalue in headcount_accuracy_df_dict_cst:
            print(f'{jvalue} exists')
        else:
            if 'daily' in jvalue:
                df_temp = pd.read_sas('{}/{}/finalfor.sas7bdat'.format(source,jvalue),
                    encoding='latin')[['SLS_TRAN_LOC_ID','DATE','PREDICT']]
                df_temp['run_date'] = datetime.strptime(jvalue[0:9], '%d%b%Y').date()
                headcount_accuracy_df_dict_cst[jvalue] = df_temp
            else:
                df_temp = pd.read_sas('{}/{}/finalfor.sas7bdat'.format(source,jvalue),
                    encoding='latin')[['SLS_TRAN_LOC_ID','week_date','PREDICT']]
                df_temp['DATE'] = df_temp['week_date']
                df_temp['run_date'] = datetime.strptime(jvalue[0:9], '%d%b%Y').date()
                headcount_accuracy_df_dict_cst[jvalue] = df_temp

# repickle your dictionary
pickle_your_object(headcount_accuracy_df_dict_cst, "headcount_accuracy_df_dict_cst")

# compile all CST forecasts and keep latest

df_dict_final_cst = {}

cst_list_keys = "df_list_daily_cst,df_list_weekly_cst".split(',')
for i in range(0,2):
    temp_dict = {}
    for (key, value) in headcount_accuracy_df_dict_cst.items():
    # Check if key is even then add pair to new dictionary
        if time_list[i] in key:
            temp_dict[key] = value
    frames = list(temp_dict.values())
    result = pd.concat(frames).sort_values(by=['SLS_TRAN_LOC_ID','DATE'])
    result = result[result['DATE'] > datetime.today() - timedelta(days=time_delta)]
    result.count()
    idx = result.groupby(by=['SLS_TRAN_LOC_ID','DATE'])['run_date'].transform(max) == result['run_date']

    df_dict_final_cst[cst_list_keys[i]] = result[idx]
    print('just finished {}'.format(cst_list_keys[i]))

pickle_your_object(df_dict_final_cst, "df_dict_final_cst")

# now for vst sigh.....

headcount_accuracy_df_dict_vst = unpickle_your_object("headcount_accuracy_df_dict_vst")
headcount_accuracy_df_dict_total = unpickle_your_object("headcount_accuracy_df_dict_total")
headcount_accuracy_df_dict_ab = unpickle_your_object("headcount_accuracy_df_dict_ab")
headcount_accuracy_df_dict_c = unpickle_your_object("headcount_accuracy_df_dict_c")
headcount_accuracy_df_dict_mt = unpickle_your_object("headcount_accuracy_df_dict_mt")



# headcount_accuracy_df_dict_vst = {}
# headcount_accuracy_df_dict_total = {}
# headcount_accuracy_df_dict_ab = {}
# headcount_accuracy_df_dict_c = {}
# headcount_accuracy_df_dict_mt = {}
#df_dict_vst = {}

#df_list_weekly_total = []
#df_list_weekly_ab = []
#df_list_weekly_c = []
#df_list_weekly_mt = []
#df_list_daily_total = []
#df_list_daily_ab = []
#df_list_daily_c = []
#df_list_daily_mt = []
type_list = 'total,ab,c,mt'.split(',')
time_list = 'daily,weekly'.split(',')

for i, ivalue in enumerate(time_list):
    file_list = [file for file in os.listdir(source) if 'run' in file and 'vst' in file and ivalue in file]

    for j, jvalue in enumerate(file_list):
        for h, hvalue in enumerate(type_list):
            if (jvalue,hvalue) in headcount_accuracy_df_dict_vst:
                print(f'{jvalue},{hvalue} exists')
            else:
                if ivalue in jvalue:
                    if 'daily' in jvalue:
                        df_temp = pd.read_sas('{}/{}/{}/finalfor.sas7bdat'.format(source,jvalue,hvalue),
                            encoding='latin')[['SLS_TRAN_LOC_ID','DATE','PREDICT']]
                        df_temp['run_date'] = datetime.strptime(jvalue[0:9], '%d%b%Y').date()
                    else:
                        df_temp = pd.read_sas('{}/{}/{}/finalfor.sas7bdat'.format(source,jvalue,hvalue),
                        encoding='latin')[['SLS_TRAN_LOC_ID','week_date','PREDICT']]
                        df_temp['DATE'] = df_temp['week_date']
                        df_temp['run_date'] = datetime.strptime(jvalue[0:9], '%d%b%Y').date()
                    if 'total' in hvalue:
                        headcount_accuracy_df_dict_total[jvalue,hvalue] = df_temp
                    elif 'ab' in hvalue:
                        headcount_accuracy_df_dict_ab[jvalue,hvalue] = df_temp
                    elif 'c' in hvalue:
                        headcount_accuracy_df_dict_c[jvalue,hvalue] = df_temp
                    else:
                        headcount_accuracy_df_dict_mt[jvalue,hvalue] = df_temp
                headcount_accuracy_df_dict_vst[jvalue,hvalue] = jvalue,hvalue

# pickle your dicts


pickle_your_object(headcount_accuracy_df_dict_vst, "headcount_accuracy_df_dict_vst")
pickle_your_object(headcount_accuracy_df_dict_total, "headcount_accuracy_df_dict_total")
pickle_your_object(headcount_accuracy_df_dict_ab, "headcount_accuracy_df_dict_ab")
pickle_your_object(headcount_accuracy_df_dict_c, "headcount_accuracy_df_dict_c")
pickle_your_object(headcount_accuracy_df_dict_mt, "headcount_accuracy_df_dict_mt")




# compile all and keep latest

list_list = [headcount_accuracy_df_dict_total,headcount_accuracy_df_dict_ab,headcount_accuracy_df_dict_c,headcount_accuracy_df_dict_mt]
vst_list_keys = "df_list_daily_total,df_list_weekly_total,df_list_daily_ab,df_list_weekly_ab,df_list_daily_c,df_list_weekly_c,df_list_daily_mt,df_list_weekly_mt".split(',')

counter = 0
df_dict_final_vst = {}
for i, ivalue in enumerate(list_list):
    for j in range(0,2):
        temp_dict = {}
        for (key, value) in ivalue.items():

        # Check if key is even then add pair to new dictionary
            if time_list[j] in key[0]:
                temp_dict[key] = value
        frames = list(temp_dict.values())

        result = pd.concat(frames).sort_values(by=['SLS_TRAN_LOC_ID','DATE'])
        result = result[result['DATE'] > datetime.today() - timedelta(days=time_delta)]
        result.count()
        idx = result.groupby(by=['SLS_TRAN_LOC_ID','DATE'])['run_date'].transform(max) == result['run_date']

        df_dict_final_vst[vst_list_keys[counter]] = result[idx]
        print('just finished {}'.format(vst_list_keys[counter]))
        counter+=1

pickle_your_object(df_dict_final_vst, "df_dict_final_vst")

#df_dict_final_vst = unpickle_your_object("df_dict_final_vst")



# Now get actuals from data

# CST actuals


headcount_actuals_df_dict_cst = {}
#df_dict_cst = {}
#df_dict_daily_cst = {}
#df_dict_weekly_cst = {}
#df_list_weekly_cst = []
#df_list_daily_cst = []
time_list = 'daily,weekly'.split(',')
for i, ivalue in enumerate(time_list):
    actuals_file = [file for file in os.listdir(source) if 'run' in file and 'cst' in file and ivalue in file and max_date in file]
    print(actuals_file)

    if 'daily' in actuals_file[0]:
        df_temp = pd.read_sas('{}/{}/outfor.sas7bdat'.format(source,actuals_file[0]),
            encoding='latin')[['SLS_TRAN_LOC_ID','DATE','ACTUAL']]
        df_temp = df_temp[(df_temp['DATE'] >  datetime.today() - timedelta(days=time_delta)) &
                        (df_temp['DATE'] <=  datetime.today())]
        df_temp = df_temp.dropna()
        print(f'{actuals_file[0]} just finished')
        headcount_actuals_df_dict_cst['{}_cst'.format(actuals_file[0])] = df_temp

    elif 'weekly' in actuals_file[0]:
        df_temp = pd.read_sas('{}/{}/outfor.sas7bdat'.format(source,actuals_file[0]),
            encoding='latin')[['SLS_TRAN_LOC_ID','week_date','ACTUAL']]
        df_temp['DATE'] = df_temp['week_date']
        df_temp = df_temp[(df_temp['DATE'] >  datetime.today() - timedelta(days=time_delta)) &
                        (df_temp['DATE'] <=  datetime.today())]
        df_temp = df_temp.dropna()
        print(f'{actuals_file[0]} just finished')
        headcount_actuals_df_dict_cst['{}_cst'.format(actuals_file[0])] = df_temp




pickle_your_object(headcount_actuals_df_dict_cst, "headcount_actuals_df_dict_cst")

#headcount_actuals_df_dict_cst = unpickle_your_object("headcount_actuals_df_dict_cst")

#now for VST sigh...


headcount_actuals_df_dict_vst = {}
headcount_actuals_df_dict_total = {}
headcount_actuals_df_dict_ab = {}
headcount_actuals_df_dict_c = {}
headcount_actuals_df_dict_mt = {}
#df_dict_vst = {}

#df_list_weekly_total = []
#df_list_weekly_ab = []
#df_list_weekly_c = []
#df_list_weekly_mt = []
#df_list_daily_total = []
#df_list_daily_ab = []
#df_list_daily_c = []
#df_list_daily_mt = []
type_list = 'total,ab,c,mt'.split(',')
time_list = 'daily,weekly'.split(',')

for i, ivalue in enumerate(time_list):
    file_list = [file for file in os.listdir(source) if 'run' in file and 'vst' in file and ivalue in file and max_date in file]
    print(file_list)
    for j, jvalue in enumerate(file_list):
        for h, hvalue in enumerate(type_list):
            if (jvalue,hvalue) in headcount_actuals_df_dict_vst:

                print(f'{jvalue},{hvalue} exists')
            else:
                if ivalue in jvalue:
                    if 'daily' in jvalue:
                        df_temp = pd.read_sas('{}/{}/{}/outfor.sas7bdat'.format(source,jvalue,hvalue),
                            encoding='latin')[['SLS_TRAN_LOC_ID','DATE','ACTUAL']]
                        df_temp = df_temp[(df_temp['DATE'] >  datetime.today() - timedelta(days=time_delta)) &
                                        (df_temp['DATE'] <=  datetime.today())]
                        df_temp['run_date'] = datetime.strptime(jvalue[0:9], '%d%b%Y').date()
                        df_temp = df_temp.dropna()
                    else:
                        df_temp = pd.read_sas('{}/{}/{}/outfor.sas7bdat'.format(source,jvalue,hvalue),
                        encoding='latin')[['SLS_TRAN_LOC_ID','week_date','ACTUAL']]
                        df_temp['DATE'] = df_temp['week_date']
                        df_temp = df_temp[(df_temp['DATE'] >  datetime.today() - timedelta(days=time_delta)) &
                                        (df_temp['DATE'] <=  datetime.today())]
                        df_temp['run_date'] = datetime.strptime(jvalue[0:9], '%d%b%Y').date()
                        df_temp = df_temp.dropna()
                    if 'total' in hvalue:
                        headcount_actuals_df_dict_total["{}_{}".format(jvalue,hvalue)] = df_temp
                    elif 'ab' in hvalue:
                        headcount_actuals_df_dict_ab["{}_{}".format(jvalue,hvalue)] = df_temp
                    elif 'c' in hvalue:
                        headcount_actuals_df_dict_c["{}_{}".format(jvalue,hvalue)] = df_temp
                    else:
                        headcount_actuals_df_dict_mt["{}_{}".format(jvalue,hvalue)] = df_temp
                    print(f'{hvalue} just finished')
                headcount_actuals_df_dict_vst["{}_{}".format(jvalue,hvalue)] = jvalue,hvalue

pickle_your_object(headcount_actuals_df_dict_vst, "headcount_actuals_df_dict_vst")
pickle_your_object(headcount_actuals_df_dict_ab, "headcount_actuals_df_dict_ab")
pickle_your_object(headcount_actuals_df_dict_c, "headcount_actuals_df_dict_c")
pickle_your_object(headcount_actuals_df_dict_mt, "headcount_actuals_df_dict_mt")
pickle_your_object(headcount_actuals_df_dict_total, "headcount_actuals_df_dict_total")

# headcount_actuals_df_dict_vst = unpickle_your_object("headcount_actuals_df_dict_vst")
# headcount_actuals_df_dict_total = unpickle_your_object("headcount_actuals_df_dict_total")
# headcount_actuals_df_dict_ab = unpickle_your_object("headcount_actuals_df_dict_ab")
# headcount_actuals_df_dict_c = unpickle_your_object("headcount_actuals_df_dict_c")
# headcount_actuals_df_dict_mt = unpickle_your_object("headcount_actuals_df_dict_mt")


# set up some iterables

type_list = 'weekly,daily'.split(',')

pred_dict_list = {
0:df_dict_final_cst,
1:df_dict_final_vst,
2:df_dict_final_vst,
3:df_dict_final_vst,
4:df_dict_final_vst,
5:df_dict_final_cst,
6:df_dict_final_vst,
7:df_dict_final_vst,
8:df_dict_final_vst,
9:df_dict_final_vst
}

pred_keys_list = {
0:'df_list_weekly_cst',
1:'df_list_weekly_total',
2:'df_list_weekly_ab',
3:'df_list_weekly_c',
4:'df_list_weekly_mt',
5:'df_list_daily_cst',
6:'df_list_daily_total',
7:'df_list_daily_ab',
8:'df_list_daily_c',
9:'df_list_daily_mt'
}

act_dict_list = {
0:headcount_actuals_df_dict_cst,
1:headcount_actuals_df_dict_total,
2:headcount_actuals_df_dict_ab,
3:headcount_actuals_df_dict_c,
4:headcount_actuals_df_dict_mt,
5:headcount_actuals_df_dict_cst,
6:headcount_actuals_df_dict_total,
7:headcount_actuals_df_dict_ab,
8:headcount_actuals_df_dict_c,
9:headcount_actuals_df_dict_mt
}

act_keys_list = {
0:f'{max_date}_cst_weekly_run_cst',
1:f'{max_date}_vst_weekly_run_total',
2:f'{max_date}_vst_weekly_run_ab',
3:f'{max_date}_vst_weekly_run_c',
4:f'{max_date}_vst_weekly_run_mt',
5:f'{max_date}_cst_daily_run_cst',
6:f'{max_date}_vst_daily_run_total',
7:f'{max_date}_vst_daily_run_ab',
8:f'{max_date}_vst_daily_run_c',
9:f'{max_date}_vst_daily_run_mt'
}




# import graphing and stats packages
from sklearn.metrics import mean_absolute_error
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot
import math
import matplotlib.backends.backend_pdf
from matplotlib.backends.backend_pdf import PdfPages

# join predition and actuals
final_dicts = {}
i = 0
for k, v in pred_keys_list.items():
    if 'week' in v:
        df_temp = pd.merge(pred_dict_list[i][pred_keys_list[i]],
                        act_dict_list[i][act_keys_list[i]], how='left', on = ['SLS_TRAN_LOC_ID','week_date'])
        df_temp.loc[:,'DATE'] = df_temp['week_date']

    if 'dai' in v:
        df_temp = pd.merge(pred_dict_list[i][pred_keys_list[i]],
                        act_dict_list[i][act_keys_list[i]], how='left', on = ['SLS_TRAN_LOC_ID','DATE'])

    print(k,v,'is just finished')
    i+=1
    final_dicts[v] = df_temp

pickle_your_object(final_dicts,'final_dicts')
final_dicts = unpickle_your_object('final_dicts')
# create reference dates for 3 time periods


month_dict_1 = {}
month_dict_3 = {}
month_dict_6 = {}
month_dict_12 = {}
for i in range(1,13):
    temp_value = i - 1
    if temp_value < 1:
        temp_value = 12
    month_dict_1[i] = temp_value


for i in range(1,13):
    temp_list = []

    for j in range(1,4):
        list_value = i - 4 + j
        if list_value < 1:
            list_value +=12
        temp_list.append(list_value)
    month_dict_3[i] = temp_list


for i in range(1,13):
    temp_list = []
    for j in range(1,7):
        list_value = i - 7 + j
        if list_value < 1:
            list_value +=12
        temp_list.append(list_value)
    month_dict_6[i] = temp_list

month_dict_12 = {}
for i in range(1,13):
    temp_list = []
    for j in range(1,12):
        list_value = i + j
        if list_value > 12:
            list_value -=12
        temp_list.append(list_value)
    month_dict_12[i] = temp_list

month_dict_12


month_dict_6b = {}
for i in range(1,13):
    temp_list = []
    temp_list2 = []
    temp_list3 = []
    for j in range(1,7):
        list_value = i - 7 + j
        if list_value > 0:
            list2_value = current_year
        else:
            list2_value = current_year - 1
        if list_value < 1:
            list_value +=12

        temp_list.append(list_value)
        temp_list2.append(list2_value)
        if list_value < 10:
            list_value = '0' + str(list_value)
        list3_value = str(list2_value) + "-" + str(list_value)
        temp_list3.append(list3_value)
    month_dict_6b[i] = [temp_list, temp_list2, temp_list3]
month_dict_6b

month_dict_12b = {}
for i in range(1,13):
    temp_list = []
    temp_list2 = []
    temp_list3 = []
    for j in range(1,12):
        list_value = i + j
        list2_value = current_year - 1
        if list_value > 12:
            list_value -=12
            list2_value = current_year
        temp_list.append(list_value)
        temp_list2.append(list2_value)
        list3_value = str(list2_value) + "-" + str(list_value)
        temp_list3.append(list3_value)
    month_dict_12b[i] = [temp_list, temp_list2, temp_list3]

month_dict_12b


def good_labels():


    daily_list_df = []
    for k,v in final_dicts.items():
        if 'daily' in k:
            daily_list_df.append(v)
    # daily_list_df_title = []
    # for k,v in final_dicts.items():
    #     if 'daily' in k:
    #         daily_list_df_title.append(k)
    daily_list_df_title = 'Daily Boss Count,Daily Total Flag Hours,Daily AB Flag Hours,Daily C Flag Hours,Daily MT Flag Hours'.split(',')

    weekly_list_df = []
    for k,v in final_dicts.items():
        if 'weekly' in k:
            weekly_list_df.append(v)
    # weekly_list_df_title = []
    # for k,v in final_dicts.items():
    #     if 'weekly' in k:
    #         weekly_list_df_title.append(k)
    weekly_list_df_title = 'Weekly Boss Count,Weekly Total Flag Hours,Weekly AB Flag Hours,Weekly C Flag Hours,Weekly MT Flag Hours'.split(',')
    return daily_list_df, daily_list_df_title, weekly_list_df, weekly_list_df_title

def good_names():

    daily_list_df = []
    for k,v in final_dicts.items():
        if 'daily' in k:
            daily_list_df.append(v)
    daily_list_df_title = []
    for k,v in final_dicts.items():
        if 'daily' in k:
            daily_list_df_title.append(k)


    weekly_list_df = []
    for k,v in final_dicts.items():
        if 'weekly' in k:
            weekly_list_df.append(v)
    weekly_list_df_title = []
    for k,v in final_dicts.items():
        if 'weekly' in k:
            weekly_list_df_title.append(k)

    return daily_list_df, daily_list_df_title, weekly_list_df, weekly_list_df_title




# set some plot parameters
a4_dims = (11.7, 8.27)
#a4_dims = (5.5, 4)
colors4 = ["#0571b0","#92c5de","#f4a582","#ca0020"]
colors3 = ["#0571b0","#92c5de","#ca0020"]


from matplotlib.patches import Patch
from matplotlib.lines import Line2D




legend_elements4 = [Patch(facecolor=colors4[0], edgecolor='black',
                         label='Great'),
                   Patch(facecolor=colors4[1], edgecolor='black',
                         label='Good'),
                   Patch(facecolor=colors4[2], edgecolor='black',
                         label='Acceptable'),
                   Patch(facecolor=colors4[3], edgecolor='black',
                         label='Questionable')]

legend_elements4a = [Patch(facecolor=colors4[0], edgecolor='black',alpha=.5,
                         label='Great'),
                   Patch(facecolor=colors4[1], edgecolor='black',alpha=.5,
                         label='Good'),
                   Patch(facecolor=colors4[2], edgecolor='black',alpha=.5,
                         label='Acceptable'),
                   Patch(facecolor=colors4[3], edgecolor='black',alpha=.5,
                         label='Questionable')]

legend_elements4b = [Patch(facecolor=colors4[0], edgecolor=colors4[0],
                         label='Great'),
                   Patch(facecolor=colors4[1], edgecolor=colors4[1],
                         label='Good'),
                   Patch(facecolor=colors4[2], edgecolor=colors4[2],
                         label='Acceptable'),
                   Patch(facecolor=colors4[3], edgecolor=colors4[3],
                         label='Questionable')]

legend_elements3 = [Patch(facecolor=colors3[0], edgecolor=colors3[0],
                         label='Great'),
                   Patch(facecolor=colors3[1], edgecolor=colors3[1],
                         label='Good'),
                   Patch(facecolor=colors3[2], edgecolor=colors3[2],
                         label='Questionable')]

daily_list_df, daily_list_df_title, weekly_list_df, weekly_list_df_title = good_labels()

# set title pre and sufix
month_lookup = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}


j = 0
with PdfPages(f'{outpath}/{max_date}_forecast_accuracy_for_weekly.pdf') as pdf_pages:

    for i, ivalue in enumerate(weekly_list_df):

        df_temp = ivalue
        df_temp.replace([np.inf, -np.inf], np.nan,inplace=True)
        df_temp = df_temp.dropna()
        df_temp = df_temp[df_temp['ACTUAL'] > 0]
        df_temp.loc[:,'ape'] = abs(df_temp['ACTUAL']-df_temp['PREDICT'])/df_temp['ACTUAL'] * 100
        #df_temp.loc[:,'full_mae'] = mean_absolute_error(df_temp['ACTUAL'],df_temp['PREDICT'])
        df_temp.loc[:,'ae'] = abs(df_temp['ACTUAL']-df_temp['PREDICT'])


        df_1_month = df_temp[df_temp['DATE'].dt.month == month_dict_1[current_month]]

        df_3_month = df_temp[df_temp['DATE'].dt.month.isin(month_dict_3[current_month])]

        df_6_month = df_temp[df_temp['DATE'].dt.month.isin(month_dict_6[current_month])]
        # df_list = {'df_1_month':[df_1_month,'Last Month']}
        if current_month == 1:
            df_list = {'df_1_month':[df_1_month,f'({month_lookup[12]})'],
                    'df_3_month':[df_3_month,'(Last 3 Months)'],
                    'df_6_month':[df_6_month,'(Last 6 Months)']}
        if current_month > 1:
            df_list = {'df_1_month':[df_1_month,f'({month_lookup[current_month-1]})'],
                    'df_3_month':[df_3_month,'(Last 3 Months)'],
                    'df_6_month':[df_6_month,'(Last 6 Months)']}

        for k,v in df_list.items():
            plt.figure(j,figsize=a4_dims)
            df = v[0].groupby('SLS_TRAN_LOC_ID').mean()
            df_question = df[df['ape'] >=101 ].to_numpy()
            df = df[(df['ape'] >=0 ) & (df['ape'] <= 100) ]
            df.loc[:,'ape_round'] =  df['ape'].round(1)
            x1 = df[df['ape_round'] <= 10]['ape_round'].to_numpy()
            x2 = df[(df['ape_round'] > 10) & (df['ape_round'] <= 20) ]['ape_round'].to_numpy()
            x3 = df[(df['ape_round'] > 20) & (df['ape_round'] <= 50) ]['ape_round'].to_numpy()
            x4 = df[(df['ape_round'] > 50) & (df['ape_round'] <= 500) ]['ape_round'].to_numpy()
            x5 = df['ape_round'].to_numpy()
            counts, bins = np.histogram(df['ape'], bins=100)
            fig, ax = pyplot.subplots(figsize=a4_dims)
            #plt.subplot2grid((5,2), (0,0), rowspan=2, colspan=2)
            ax.hist(x1, bins=11, color=colors4[0],histtype="bar",edgecolor='black')
            ax.hist(x2, bins=10, color=colors4[1],histtype="bar",edgecolor='black')
            ax.hist(x3, bins=30, color=colors4[2],histtype="bar",edgecolor='black')
            ax.hist(x4, bins=50, color=colors4[3],histtype="bar",edgecolor='black')
            #ax.hist(x5, bins=100, color='#d7191c',histtype='bar',density=True)
            #ax.set(xlabel="MAPE", ylabel="Counts", title='')
            #sns.distplot(df['ape_round'], hist=False)
            #plt.savefig(f'/data2/users/jbackes/{weekly_list_df_title[i]} - {v[1]}.pdf')
            matplotlib.rc('xtick', labelsize=12)
            plt.xlabel('Mean Average Percent Error (MAPE)', fontsize=18)
            plt.ylabel('Count', fontsize=18)
            matplotlib.rc('ytick', labelsize=12)
            fig.legend(title='Accuracy Level',handles=legend_elements4, loc='upper right', bbox_to_anchor=(0.9, 0.88),shadow=True, fontsize='large')
            pre = 'Distribution of MAPE'
            fig.suptitle(f'{pre}\n{weekly_list_df_title[i]} - {v[1]}', fontsize=20, y=.97)
            fig.text(0.02, .02, f'Page {str(j+1)}', ha='left', va='bottom', transform=fig.transFigure, fontsize=12)
            pdf_pages.savefig(fig)

            j+=1
            plt.clf()
            plt.figure(figsize=a4_dims)
            bar1 = len(x1)
            bar2 = len(x2)
            bar3 = len(x3)
            bar4 = len(x4)+len(df_question)
            bar5 = len(x4)
            bar6 = len(df_question)

            #print(bar4)
            #print(bar5)
            #print(bar6)
            xaxis = 'Great,Good,Acceptable,Questionable'.split(',')

            yaxis = [bar1,bar2,bar3,bar4]

            d = {'Accuracy Level':xaxis,'Store Count':yaxis}
            df = pd.DataFrame(d)
            pre = 'Store Count by Accuracy Level'
            custom_palette = sns.set_palette(sns.color_palette(colors4))
            #plt.figure(figsize=a4_dims)
            plot2a = sns.barplot(x = 'Accuracy Level', y = 'Store Count', data=df, edgecolor='black', palette=custom_palette)
            plot2 = sns.barplot(x = 'Accuracy Level', y = 'Store Count', data=df, edgecolor='black', palette=custom_palette).get_figure()
            for p in plot2a.patches:
                if p.get_height() < 200:
                    plot2a.annotate(format(p.get_height(), '.0f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        size=15,
                        xytext = (0, 9),
                        textcoords = 'offset points')
                else:
                    plot2a.annotate(format(p.get_height(), '.0f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        size=15,
                        xytext = (0, -12),
                        textcoords = 'offset points')
  
            plot2.suptitle(f'{pre}\n{weekly_list_df_title[i]} - {v[1]}', fontsize=20, y=.97)
            plt.xlabel('Accuracy Level', fontsize=18)
            plt.ylabel('Store Count', fontsize=18)
            plot2.legend(title='Accuracy Level',handles=legend_elements4, loc='upper right', bbox_to_anchor=(0.9, 0.88),shadow=True, fontsize='large')
            plot2.text(0.02, .02, f'Page {str(j+1)}', ha='left', va='bottom', transform=fig.transFigure, fontsize=12)

            pdf_pages.savefig(plot2)
            j+=1
            plt.clf()
            #plt.savefig(f'/data2/users/jbackes/{weekly_list_df_title[i]} - {v[1]}_bar.pdf')





stats_dict = {0:[5,7,9],
            1:[8,12,15],
            2:[3,5,7.5],
            3:[3.5,4.5,5.5],
            4:[3,5,6]}
stats_dict = {0:[5,7,9],
            1:[8,12,16],
            2:[2,5,8],
            3:[3,5,7],
            4:[3,5,7]}
stats_dict = {0:[5,7,9],
            1:[8,12,16],
            2:[2,5,8],
            3:[3,5,7],
            4:[3,5,7]}
stats_dict = {0:[4,6,8],
            1:[7,11,15],
            2:[1,4,7],
            3:[2,4,6],
            4:[2,4,6]}
stats_dict = {0:[5,7,9],
            1:[7,10,14],
            2:[2,4,7],
            3:[3,5,7],
            4:[3,4,6]}
stats_dict = {0:[4.8,7.2,9.6],
            1:[8.5,12.7,17],
            2:[1.7,2.6,3.5],
            3:[3,4.5,5.9],
            4:[3.6,5.4,7.2]}



j = 0
with PdfPages(f'{outpath}/{max_date}_forecast_accuracy_for_daily.pdf') as pdf_pages:


    for i, ivalue in enumerate(daily_list_df):
        df_temp = ivalue
        df_temp.replace([np.inf, -np.inf], np.nan,inplace=True)
        df_temp = df_temp.dropna()
        df_temp = df_temp[df_temp['ACTUAL'] > 0]
        df_temp.loc[:,'ape'] = abs(df_temp['ACTUAL']-df_temp['PREDICT'])/df_temp['ACTUAL'] * 100
        #df_temp.loc[:,'full_mae'] = mean_absolute_error(df_temp['ACTUAL'],df_temp['PREDICT'])
        df_temp.loc[:,'ae'] = abs(df_temp['ACTUAL']-df_temp['PREDICT'])

    #df_1_month['ae'].describe()
    #df_1_month['ae'].quantile([.95])
    #df_1_month['ACTUAL'].describe()
        df_1_month = df_temp[df_temp['DATE'].dt.month == month_dict_1[current_month]]

        df_3_month = df_temp[df_temp['DATE'].dt.month.isin(month_dict_3[current_month])]

        df_6_month = df_temp[df_temp['DATE'].dt.month.isin(month_dict_6[current_month])]

        #df_list = {'df_1_month':[df_1_month,'Last Month']}
        if current_month == 1:
            df_list = {'df_1_month':[df_1_month,f'({month_lookup[12]})'],
                    'df_3_month':[df_3_month,'(Last 3 Months)'],
                    'df_6_month':[df_6_month,'(Last 6 Months)']}
        if current_month > 1:
            df_list = {'df_1_month':[df_1_month,f'({month_lookup[current_month-1]})'],
                    'df_3_month':[df_3_month,'(Last 3 Months)'],
                    'df_6_month':[df_6_month,'(Last 6 Months)']}
        for k,v in df_list.items():
            df = v[0].groupby('SLS_TRAN_LOC_ID').mean()

            #sns.distplot(df['ae'])
            qmin = df['ae'].quantile([.00]).values[0].round(2)
            q1 =  df['ae'].quantile([.01]).values[0].round(2)
            q5 =  df['ae'].quantile([.05]).values[0].round(2)
            q10 =  df['ae'].quantile([.10]).values[0].round(2)
            q25 = df['ae'].quantile([.25]).values[0].round(2)
            q50 = df['ae'].quantile([.50]).values[0].round(2)
            q75 = df['ae'].quantile([.75]).values[0].round(2)
            q90 = df['ae'].quantile([.90]).values[0].round(2)
            q95 = df['ae'].quantile([.95]).values[0].round(2)
            q99 = df['ae'].quantile([.99]).values[0].round(2)
            qmax = df['ae'].quantile([1.]).values[0].round(2)
            print(daily_list_df_title[i], '---', qmin, q1, q5, q10, q25, q50, q75, q90, q95, q99, qmax)
            s4 = q90/3
            # print(s4)
            df = df[(df['ae'] >=0 ) & (df['ae'] <= q99) ]
            df.loc[:,'mae_round'] =  df['ae'].round(1)
            x1 = df[(df['mae_round'] >= 0) & (df['mae_round'] <= stats_dict[i][0]) ]['mae_round'].to_numpy()
            x2 = df[(df['mae_round'] > stats_dict[i][0]) & (df['mae_round'] <= stats_dict[i][1]) ]['mae_round'].to_numpy()
            x3 = df[(df['mae_round'] > stats_dict[i][1]) & (df['mae_round'] <= stats_dict[i][2]) ]['mae_round'].to_numpy()
            x4 = df[(df['mae_round'] > stats_dict[i][2]) & (df['mae_round'] <= q99) ]['mae_round'].to_numpy()


            fig = plt.figure(figsize=a4_dims)
            matplotlib.rc('xtick', labelsize=12)
            plt.xlabel('Mean Absolute Error (MAE)', fontsize=18)
            plt.ylabel('Count', fontsize=18)
            matplotlib.rc('ytick', labelsize=12)
            ax = plt.hist(df['mae_round'],bins=30, edgecolor='black', color='white')

                        
            # plot1 = sns.distplot(df['mae_round']).get_figure()
            plt.axvspan(qmin, stats_dict[i][0], color=colors4[0], alpha=.5)
            plt.axvspan(stats_dict[i][0], stats_dict[i][1], color=colors4[1], alpha=.5)
            plt.axvspan(stats_dict[i][1], stats_dict[i][2], color=colors4[2], alpha=.5)
            plt.axvspan(stats_dict[i][2], q99, color=colors4[3], alpha=.5)
            plt.legend(title='Accuracy Level', handles=legend_elements4a, loc='upper right', bbox_to_anchor=(0.99, 0.99),shadow=True, fontsize='large')
            pre = 'Distribution of MAE'
            fig.suptitle(f'{pre}\n{daily_list_df_title[i]} - {v[1]}', fontsize=20, y=.97)
            fig.text(0.02, .02, f'Page {str(j+1)}', ha='left', va='bottom', transform=fig.transFigure, fontsize=12)
            



            pdf_pages.savefig(fig)

            j+=1
            plt.clf()
            fig = plt.figure(figsize=a4_dims)
            bar1 = len(x1)
            bar2 = len(x2)
            bar3 = len(x3)
            bar4 = len(x4)
            # print(bar4)
            # print(bar5)
            # print(bar6)


            xaxis = 'Great,Good,Acceptable,Questionable'.split(',')
            yaxis = [bar1,bar2,bar3,bar4]

            d = {'Accuracy Level':xaxis,'Store Count':yaxis}
            df = pd.DataFrame(d)
            pre = 'Store Count by Accuracy Level'
            custom_palette = sns.set_palette(sns.color_palette(colors4))
            #plt.figure(figsize=a4_dims)
            ax = sns.barplot(x = 'Accuracy Level', y = 'Store Count', edgecolor='black', data=df, palette=custom_palette)
            for p in ax.patches:
                if p.get_height() < 200:
                    ax.annotate(format(p.get_height(), '.0f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        size=15,
                        xytext = (0, 9),
                        textcoords = 'offset points')
                else:
                    ax.annotate(format(p.get_height(), '.0f'), 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha = 'center', va = 'center', 
                        size=15,
                        xytext = (0, -12),
                        textcoords = 'offset points')
            ax.set_xlabel('Accuracy Level', fontsize=18)
            ax.set_ylabel('Store Count', fontsize=18)
            plt.suptitle(f'{pre}\n{daily_list_df_title[i]} - {v[1]}', fontsize=20, y=.97)
            plt.legend(title='Accuracy Level',handles=legend_elements4, loc='upper right', bbox_to_anchor=(0.99, 0.99),shadow=True, fontsize='large')
            plt.text(0.02, .02, f'Page {str(j+1)}', ha='left', va='bottom', transform=fig.transFigure, fontsize=12)
            pdf_pages.savefig(fig)
            j+=1
            plt.clf()
# import pandas as pd
# df = pd.read_sas("/data2/bsro/030_IBP_Forecasting_Model_2015/production/strategic/st_prod/d_reports/forecast.sas7bdat",
#             encoding='latin1')
# df.head()
# df.columns
# df.to_csv("/data2/Common/BSRO Supply Chain/Forecast/forcast.csv")

# file = 'loc_store_area_cd'

# df = pd.read_sas(f"/data2/bsro/030_IBP_Forecasting_Model_2015/production/strategic/c_landing/{file}_desc.sas7bdat",
#             encoding='latin1')

# df.to_csv(f"/data2/Common/BSRO Supply Chain/Forecast/{file}_desc.csv")

# file = 'outest_t_bucket1'

# df = pd.read_sas(f"/data2/bsro/030_IBP_Forecasting_Model_2015/production/strategic/st_prod/d_model/{file}.sas7bdat",
#             encoding='latin1')

# df.to_csv(f"/data2/Common/BSRO Supply Chain/Forecast/{file}.csv")


# file = 'store_month_attributes'
# itr = pd.read_sas(f"/data2/bsro/030_IBP_Forecasting_Model_2015/production/strategic/c_landing/{file}.sas7bdat",
#             encoding='latin1', chunksize=100)
# for chunk in itr:
#     df = chunk
#     break

# df.head()


# df.to_csv(f"/data2/Common/BSRO Supply Chain/Forecast/{file}.csv")

# month reference table


current_month = 12
month_lookup = {}
for k,v in month_dict_6b.items():
    if k == current_month:
        i = current_month - 6
        for j in v[2]:
            month_lookup[i] = j
            i+=1
        print(v[2])
month_dict_6


# weekly trend line accuracy
month_lookup
daily_list_df, daily_list_df_title, weekly_list_df, weekly_list_df_title = good_names()

# Weely trend line dictionary
trend_line_dict_weekly = {}
for i, ivalue in enumerate(weekly_list_df):

    df_temp = ivalue
    df_temp.replace([np.inf, -np.inf], np.nan,inplace=True)
    df_temp = df_temp.dropna()
    df_temp = df_temp[df_temp['ACTUAL'] > 0]
    df_temp.loc[:,'ape'] = abs(df_temp['ACTUAL']-df_temp['PREDICT'])/df_temp['ACTUAL'] * 100
    #df_temp.loc[:,'full_mae'] = mean_absolute_error(df_temp['ACTUAL'],df_temp['PREDICT'])
    df_temp.loc[:,'ae'] = abs(df_temp['ACTUAL']-df_temp['PREDICT'])
    month_list = []
    x1_list = []
    x2_list = []
    x3_list = []
    x4_list = []
    for j in month_dict_6[current_month]:
        temp_dict = {}
        temp_list = []
        df_month_temp = df_temp[df_temp['DATE'].dt.month == j]
        df = df_month_temp.groupby('SLS_TRAN_LOC_ID').mean()
        df_question = df[df['ape'] >=101 ].to_numpy()
        df = df[(df['ape'] >=0 ) & (df['ape'] <= 100) ]
        df.loc[:,'ape_round'] =  df['ape'].round(1)
        month_list.append(month_lookup[j])
        x1_list.append(len(df[df['ape_round'] <= 10]['ape_round'].to_numpy()))
        x2_list.append(len(df[(df['ape_round'] > 10) & (df['ape_round'] <= 20) ]['ape_round'].to_numpy()))
        x3_list.append(len(df[(df['ape_round'] > 20) & (df['ape_round'] <= 50) ]['ape_round'].to_numpy()))
        x4_list.append(len(df[(df['ape_round'] > 50) & (df['ape_round'] <= 500) ]['ape_round'].to_numpy()))
    temp_dict['month'] = month_list
    temp_dict['x1'] = x1_list
    temp_dict['x2'] = x2_list
    temp_dict['x3'] = x3_list
    temp_dict['x4'] = x4_list

    trend_line_dict_weekly[weekly_list_df_title[i]] = temp_dict




# for k, v in trend_line_dict_weekly.items():
#     for k2, v2, in v.items():
#         for i, ivalue in enumerate(v2):
#             print('ivalue',ivalue)
#             print('dict',archive_trend_line_dict_weekly[k][k2])


#                for k2, v2, in v.items():
#         for i, ivalue in enumerate(v

#archive_trend_line_dict_weekly = trend_line_dict_weekly

# df_dict_weekly_archive = {}

# for k,v in trend_line_dict_weekly_archive.items():
#     temp_dict = pd.DataFrame(v, columns = 'month,x1,x2,x3,x4'.split(','))
#     df_dict_weekly_archive[k] = temp_dict
# df_dict_weekly_archive

df_dict_weekly_archive = unpickle_your_object('df_dict_weekly_archive')



df_dict_weekly = {}
for k,v in trend_line_dict_weekly.items():
    temp_dict = pd.DataFrame(v, columns = 'month,x1,x2,x3,x4'.split(','))
    df_dict_weekly[k] = temp_dict

#df_dict_weekly_archive = df_dict_weekly

new_dict_weekly = {}
frames_list = []
for k, v in df_dict_weekly_archive.items():
    frames = [v,df_dict_weekly[k]]
    df = pd.concat(frames)
    df = df.drop_duplicates(subset='month', keep='last')
    new_dict_weekly[k] = df




pickle_your_object(new_dict_weekly, "df_dict_weekly_archive")



new_dict_weeklyb = {}
for k,v in new_dict_weekly.items():
    df = v[v['month'].isin(month_list)]
    new_dict_weeklyb[k] = df

new_dict_weeklyb

daily_list_df, daily_list_df_title, weekly_list_df, weekly_list_df_title = good_labels()

pre = "Count of Stores by Accuracy Level Over Time"

a4_dims = (15, 8)

i = 0
with PdfPages(f'{outpath}/{max_date}_accuracy_trend_for_weekly.pdf') as pdf_pages:
    for k,v in trend_line_dict_weekly.items():



        plt.figure(figsize=a4_dims)
        plt.plot( 'month', 'x1', data=new_dict_weeklyb[k], marker='o', markerfacecolor=colors4[0], markersize=12, color=colors4[0], linewidth=4)
        plt.plot( 'month', 'x2', data=new_dict_weeklyb[k], marker='o', markerfacecolor=colors4[1], markersize=12, color=colors4[1], linewidth=4)
        plt.plot( 'month', 'x3', data=new_dict_weeklyb[k], marker='o', markerfacecolor=colors4[2], markersize=12, color=colors4[2], linewidth=4)
        plt.plot( 'month', 'x4', data=new_dict_weeklyb[k], marker='o', markerfacecolor=colors4[3], markersize=12, color=colors4[3], linewidth=4)
        matplotlib.rc('xtick', labelsize=12)
        plt.xlabel('Month', fontsize=18)
        plt.ylabel('Store Count', fontsize=18)
        matplotlib.rc('ytick', labelsize=12)
        plt.legend(title='Accuracy Level', handles=legend_elements4b, loc='upper left', bbox_to_anchor=(0.01, 0.98),shadow=True, fontsize='large')
        plt.suptitle(f'{pre}\n({weekly_list_df_title[i]})', fontsize=20, y=.96)
        plt.text(0.02, .02, 'Page 1', ha='left', va='bottom', transform=fig.transFigure, fontsize=12)

        pdf_pages.savefig()
        i+=1


#daily




daily_list_df, daily_list_df_title, weekly_list_df, weekly_list_df_title = good_names()

# daily trend line dictionary
trend_line_dict_daily = {}
for i, ivalue in enumerate(daily_list_df):

    df_temp = ivalue
    df_temp.replace([np.inf, -np.inf], np.nan,inplace=True)
    df_temp = df_temp.dropna()
    df_temp = df_temp[df_temp['ACTUAL'] > 0]
    df_temp.loc[:,'ape'] = abs(df_temp['ACTUAL']-df_temp['PREDICT'])/df_temp['ACTUAL'] * 100
    #df_temp.loc[:,'full_mae'] = mean_absolute_error(df_temp['ACTUAL'],df_temp['PREDICT'])
    df_temp.loc[:,'ae'] = abs(df_temp['ACTUAL']-df_temp['PREDICT'])
    month_list = []
    x1_list = []
    x2_list = []
    x3_list = []
    x4_list = []
    for j in month_dict_6[current_month]:
        temp_dict = {}
        temp_list = []
        df_month_temp = df_temp[df_temp['DATE'].dt.month == j]
        df = df_month_temp.groupby('SLS_TRAN_LOC_ID').mean()


        # q25 = df['ae'].quantile([.25]).values[0].round(2)
        # q90 = df['ae'].quantile([.90]).values[0].round(2)
        # q95 = df['ae'].quantile([.95]).values[0].round(2)
        q99 = df['ae'].quantile([.99]).values[0].round(2)
        qmax = df['ae'].max()
        # print(q90, q95, q99)
        # s4 = q90/3
        # print(s4)
        df = df[(df['ae'] >=0 ) & (df['ae'] <= q99) ]
        df.loc[:,'mae_round'] =  df['ae'].round(1)
        #print(df.describe())
        df_question = df[df['ape'] > q99+1 ].to_numpy()
        #if k == 'df_1_month':
        #    if daily_list_df_title[i] == 'df_list_daily_cst':
        #        df_delete = df
        x2_range = math.ceil(q90-q25)
        x3_range = math.ceil(q99+1-q25)
        x1_range = int(round(q25,0))
        x1_list.append(len(df[df['mae_round'] <= stats_dict[i][0]]['mae_round'].to_numpy()))
        x2_list.append(len(df[(df['mae_round'] > stats_dict[i][0]) & (df['mae_round'] <= stats_dict[i][1]) ]['mae_round'].to_numpy()))
        x3_list.append(len(df[(df['mae_round'] > stats_dict[i][1]) & (df['mae_round'] <= stats_dict[i][2]) ]['mae_round'].to_numpy()))
        x4_list.append(len(df[(df['mae_round'] > stats_dict[i][2]) & (df['mae_round'] <= q99) ]['mae_round'].to_numpy()))
        month_list.append(month_lookup[j])

    temp_dict['month'] = month_list
    temp_dict['x1'] = x1_list
    temp_dict['x2'] = x2_list
    temp_dict['x3'] = x3_list
    temp_dict['x4'] = x4_list

    trend_line_dict_daily[daily_list_df_title[i]] = temp_dict


df_dict_daily_archive = unpickle_your_object('df_dict_daily_archive')


df_dict_daily = {}
for k,v in trend_line_dict_daily.items():
    temp_dict = pd.DataFrame(v, columns = 'month,x1,x2,x3,x4'.split(','))
    df_dict_daily[k] = temp_dict

#df_dict_daily_archive = df_dict_daily

new_dict_daily = {}
frames_list = []
for k, v in df_dict_daily_archive.items():
    frames = [v,df_dict_daily[k]]
    df = pd.concat(frames)
    df = df.drop_duplicates(subset='month', keep='last')
    new_dict_daily[k] = df

pickle_your_object(new_dict_daily, "df_dict_daily_archive")



new_dict_dailyb = {}
for k,v in new_dict_daily.items():
    df = v[v['month'].isin(month_list)]
    new_dict_dailyb[k] = df

new_dict_dailyb

daily_list_df, daily_list_df_title, weekly_list_df, weekly_list_df_title = good_labels()

a4_dims = (15, 8)
pre = "Count of Stores by Accuracy Level Over Time"
i = 0
with PdfPages(f'{outpath}/{max_date}_accuracy_trend_for_daily.pdf') as pdf_pages:
    for k,v in trend_line_dict_daily.items():


        plt.figure(figsize=a4_dims)
        plt.plot( 'month', 'x1', data=new_dict_dailyb[k], marker='o', markerfacecolor=colors4[0], markersize=12, color=colors4[0], linewidth=4)
        plt.plot( 'month', 'x2', data=new_dict_dailyb[k], marker='o', markerfacecolor=colors4[1], markersize=12, color=colors4[1], linewidth=4)
        plt.plot( 'month', 'x3', data=new_dict_dailyb[k], marker='o', markerfacecolor=colors4[2], markersize=12, color=colors4[2], linewidth=4)
        plt.plot( 'month', 'x4', data=new_dict_dailyb[k], marker='o', markerfacecolor=colors4[3], markersize=12, color=colors4[3], linewidth=4)
        matplotlib.rc('xtick', labelsize=12)
        plt.xlabel('Month', fontsize=18)
        plt.ylabel('Store Count', fontsize=18)
        matplotlib.rc('ytick', labelsize=12)
        plt.legend(title='Accuracy Level', handles=legend_elements4b, loc='upper left', bbox_to_anchor=(0.01, 0.98),shadow=True, fontsize='large')
        plt.suptitle(f'{pre}\n({daily_list_df_title[i]})', fontsize=20, y=.96)
        plt.text(0.02, .02, 'Page 1', ha='left', va='bottom', transform=fig.transFigure, fontsize=12)
        pdf_pages.savefig()
       # plt.savefig(f'/data2/bsro/00028_ld_mvp1/output/accuracy_reports/{max_date}_{daily_list_df_title[i]}.pdf')
        i+=1

        
 def day_of_week_order(x):
    if (x['weekday'] == 'Saturday'):
        return 1
    if (x['weekday'] == 'Monday'):
        return 2
    if (x['weekday'] == 'Tuesday'):
        return 3
    if (x['weekday'] == 'Wednesday'):
        return 4
    if (x['weekday'] == 'Thursday'):
        return 5
    if (x['weekday'] == 'Friday'):
        return 6

