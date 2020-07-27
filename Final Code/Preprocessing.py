## AS ORIGINAL DATA IS NOT BEEN PROVIDED WITH THE SUBBMISSION, PLEASE COPY 
## THE ORIGINAL DATASET INTO THE SAME FOLDER AS THIS CODE BEFORE 
## EXECUTING.

import numpy as np
import pandas as pd

# Importing Dataset
df = pd.read_csv("train_upd.csv")

# Merging Date-Time
df['date']=df['par_day'].map(str)+"/"+df['par_month'].map(str)+"/"+df['par_year'].map(str)
df['par_min'] = df['par_min'] - 5
df['time'] = df['par_hour'].map(str) + ":" + df['par_min'].map(str)
df['day-time'] = df['date'].map(str) + " " + df['time'].map(str)

# Merging all the data features and taking LOG of all the features
data_features = ['web_browsing_total_bytes','video_total_bytes', 'social_ntwrking_bytes',
       'cloud_computing_total_bytes', 'web_security_total_bytes',
       'gaming_total_bytes', 'health_total_bytes', 'communication_total_bytes',
       'file_sharing_total_bytes', 'remote_access_total_bytes',
       'photo_sharing_total_bytes', 'software_dwnld_total_bytes',
       'marketplace_total_bytes', 'storage_services_total_bytes',
       'audio_total_bytes', 'location_services_total_bytes',
       'presence_total_bytes', 'advertisement_total_bytes',
       'system_total_bytes', 'voip_total_bytes', 'speedtest_total_bytes',
       'email_total_bytes', 'weather_total_bytes', 'media_total_bytes',
       'mms_total_bytes', 'others_total_bytes', "subscriber_count"]
df['total_data'] = df[data_features].sum(axis = 1)
df['log(total_data)'] = np.log(df['total_data'] + 1)

for col in data_features:
    df["log( " + col + " )"] = np.log(df[col]+1)

# Creating MAJOR, MINOR and other features        
major1 = ['web_browsing_total_bytes','video_total_bytes', 'social_ntwrking_bytes']
major2 = ['cloud_computing_total_bytes','communication_total_bytes','presence_total_bytes']

minor = ['web_security_total_bytes',
       'gaming_total_bytes', 'health_total_bytes', 
       'file_sharing_total_bytes', 'remote_access_total_bytes',
       'photo_sharing_total_bytes', 'software_dwnld_total_bytes',
       'marketplace_total_bytes', 'storage_services_total_bytes',
       'audio_total_bytes', 'location_services_total_bytes',
        'advertisement_total_bytes',
       'system_total_bytes', 'voip_total_bytes', 'speedtest_total_bytes',
       'email_total_bytes', 'weather_total_bytes', 'media_total_bytes',
       'mms_total_bytes', 'others_total_bytes']

df['MAJOR(1)'] = df[major1].sum(axis = 1)
df['MAJOR(2)'] = df[major2].sum(axis = 1)
df['MINOR'] = df[minor].sum(axis = 1)

df['MAJOR(1)/MINOR'] = df['MAJOR(1)']/df['MINOR']
df['MAJOR(2)/MINOR'] = df['MAJOR(2)']/df['MINOR']
df["log(minor)"] = np.log(df['MINOR'])

# Calculating total_data/subs_count
df['total_data/subs_count'] = df["total_data"]/df["subscriber_count"]
df['LOG(total_data/subs_count)'] = np.log(df['total_data/subs_count'])

# Creating weekend feature
df["mod_day"] = df["par_day"] % 7
df.loc[df.mod_day <= 2 , "weekend"] = 1
df.loc[df.mod_day > 2 , "weekend"] = 0

# One-hot encoding ran_vendor
df = pd.concat([df, pd.get_dummies(df["ran_vendor"])], axis = 1)

# One-hot encode different interval of day
df.loc[df.par_hour <= 7 , "day_part"] = "night"
df.loc[(df.par_hour <= 17) & (7 < df.par_hour), "day_part"] = "work"
df.loc[(df.par_hour <= 23) & (17 < df.par_hour), "day_part"] = "evening"

df = pd.concat([df, pd.get_dummies(df["day_part"])], axis = 1)

# Droping useless columns
df = df.drop(["mod_day", "day_part"], axis = 1)

df.to_csv("modified_data.csv", index = False)

#------------------------  Preprocessing Test Data  -----------------------------------#
# Importing Dataset
df = pd.read_csv("test_upd.csv")

# Merging Date-Time
df['date']=df['par_day'].map(str)+"/"+df['par_month'].map(str)+"/"+df['par_year'].map(str)
df['par_min'] = df['par_min'] - 5
df['time'] = df['par_hour'].map(str) + ":" + df['par_min'].map(str)
df['day-time'] = df['date'].map(str) + " " + df['time'].map(str)

# Merging all the data features and taking LOG of all the features
data_features = ['web_browsing_total_bytes','video_total_bytes', 'social_ntwrking_bytes',
       'cloud_computing_total_bytes', 'web_security_total_bytes',
       'gaming_total_bytes', 'health_total_bytes', 'communication_total_bytes',
       'file_sharing_total_bytes', 'remote_access_total_bytes',
       'photo_sharing_total_bytes', 'software_dwnld_total_bytes',
       'marketplace_total_bytes', 'storage_services_total_bytes',
       'audio_total_bytes', 'location_services_total_bytes',
       'presence_total_bytes', 'advertisement_total_bytes',
       'system_total_bytes', 'voip_total_bytes', 'speedtest_total_bytes',
       'email_total_bytes', 'weather_total_bytes', 'media_total_bytes',
       'mms_total_bytes', 'others_total_bytes', "subscriber_count"]
df['total_data'] = df[data_features].sum(axis = 1)
df['log(total_data)'] = np.log(df['total_data'] + 1)

for col in data_features:
    df["log( " + col + " )"] = np.log(df[col]+1)

# Creating MAJOR, MINOR and other features        
major1 = ['web_browsing_total_bytes','video_total_bytes', 'social_ntwrking_bytes']
major2 = ['cloud_computing_total_bytes','communication_total_bytes','presence_total_bytes']

minor = ['web_security_total_bytes',
       'gaming_total_bytes', 'health_total_bytes', 
       'file_sharing_total_bytes', 'remote_access_total_bytes',
       'photo_sharing_total_bytes', 'software_dwnld_total_bytes',
       'marketplace_total_bytes', 'storage_services_total_bytes',
       'audio_total_bytes', 'location_services_total_bytes',
        'advertisement_total_bytes',
       'system_total_bytes', 'voip_total_bytes', 'speedtest_total_bytes',
       'email_total_bytes', 'weather_total_bytes', 'media_total_bytes',
       'mms_total_bytes', 'others_total_bytes']

df['MAJOR(1)'] = df[major1].sum(axis = 1)
df['MAJOR(2)'] = df[major2].sum(axis = 1)
df['MINOR'] = df[minor].sum(axis = 1)

df['MAJOR(1)/MINOR'] = df['MAJOR(1)']/df['MINOR']
df['MAJOR(2)/MINOR'] = df['MAJOR(2)']/df['MINOR']
df["log(minor)"] = np.log(df['MINOR'])

# Calculating total_data/subs_count
df['total_data/subs_count'] = df["total_data"]/df["subscriber_count"]
df['LOG(total_data/subs_count)'] = np.log(df['total_data/subs_count'])

# Creating weekend feature
df["mod_day"] = df["par_day"] % 7
df.loc[df.mod_day <= 2 , "weekend"] = 1
df.loc[df.mod_day > 2 , "weekend"] = 0

# One-hot encoding ran_vendor
df = pd.concat([df, pd.get_dummies(df["ran_vendor"])], axis = 1)

# One-hot encode different interval of day
df.loc[df.par_hour <= 7 , "day_part"] = "night"
df.loc[(df.par_hour <= 17) & (7 < df.par_hour), "day_part"] = "work"
df.loc[(df.par_hour <= 23) & (17 < df.par_hour), "day_part"] = "evening"

df = pd.concat([df, pd.get_dummies(df["day_part"])], axis = 1)

# Droping useless columns
df = df.drop(["mod_day", "day_part"], axis = 1)

# dumping csv file
df.to_csv("modified_data_test.csv", index = False)

