#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:39:37 2020

@author: brento

2019 Novel Coronavirus COVID-19 (2019-nCoV) 
Data Repository by Johns Hopkins CSSE (GitHub)

This code clones the repo and pulls the daily data uploaded.
The created folders are "COVID19_REPO" and "COVID19_GlobalDaily"

Date Range: 01-22-2020 to today (04-17-2020)
"""

import os
import os.path
import git 
import pandas as pd 
# import glob
# from datetime import date
# import matplotlib.pyplot as plt


# delete old folder and replace with updated data
def deleteOld(path, raw, daily):
    os.chdir(path)
    if(os.path.isdir(raw)):
        os.system('rm -r ' + raw)
    
    if(os.path.isdir(daily)):
        os.system('rm -r ' + daily)
        

# clones repo to folder on Desktop
# takes about 4 min to run
def cloneRepo(git_repo, path, new_folder):
    os.chdir('/') # have to set back to base dir idk why
    git.Repo.clone_from(git_repo, path + new_folder,
      branch='master', depth=1,
      env={'GIT_SSL_NO_VERIFY': '1'},
    )


# extract the needed data from repo and copy to folder
def copyDaily(subfolder_path, copy_path):
    os.chdir(subfolder_path)
    
    # copy needed csv to new folder
    os.system("cp -R " + subfolder_path + " " + copy_data_path)



# load csv, add dates, and aggregate
# CHANGE COLUMN NAMES ON 3-22-2020
# creates a aggregate df based on country and date
def mergeDF(copy_path):
    name = ""
    full_df_raw = pd.DataFrame()
    
    directory = os.path.join(copy_path)
    for root,dirs,files in os.walk(directory):
        for file in files:
           if file.endswith(".csv"):
               data = pd.read_csv(file) 
               # Declare a list that is to be converted into a column 
               rows = len(data)
               name = str(file.split('.')[0])
               # add date column for easier aggregation
               dates = [name] * rows
               data['Date'] = dates
               # d=columns names mismatched from this date forward
               if(name < "03-22-2020"):
                   if('Country/Region' in data.columns):
                       data['Country_Region'] = data['Country/Region']
                       data = data.drop(['Country/Region'], axis=1)
                   if('Latitude' in data.columns):
                       data['Lat'] = data['Latitude']
                       data = data.drop(['Latitude'], axis=1)
                   if('Longitude' in data.columns):
                       data['Long_'] = data['Longitude']
                       data = data.drop(['Longitude'], axis=1)
                   if('Province/State' in data.columns):
                       data['Province_State'] = data['Province/State']
                       data = data.drop(['Province/State'], axis=1)
               full_df_raw = full_df_raw.append(pd.DataFrame(data = data), 
                                                ignore_index=True)
           
    # Admin2, Combined_Key, Confirmed, Country_Region, Date, Deaths, Lat, Long_
    # Province_State, Recovered
    
    full_df_trim = full_df_raw[['Admin2', 'Combined_Key', 'Confirmed', 
                               'Country_Region', 'Date', 'Deaths', 'Lat', 'Long_',
                               'Province_State', 'Recovered']]
    
    for i in range(0,len(full_df_trim['Country_Region'])):
        if(full_df_trim['Country_Region'][i] == 'Mainland China'):
            full_df_trim['Country_Region'][i] = 'China'
    return(full_df_trim)
        

def groupbyCountry(full_df):
    group_confirmed = full_df.groupby(['Country_Region', 'Date']).agg({'Confirmed': ['sum']})
    group_deaths = full_df.groupby(['Country_Region', 'Date']).agg({'Deaths': ['sum']})
    group_recovered = full_df.groupby(['Country_Region', 'Date']).agg({'Recovered': ['sum']})
    
    all_metrics_df = group_recovered.join(group_confirmed.join(group_deaths))
    # check for na and misjoin
    # all_metrics_df.isna().sum()
    return(all_metrics_df)


# plot metric by country over dates given
# create country, date columns and input statistics
def plotMetric(all_metrics_df, country_name, stat):
    country_df = pd.DataFrame()
    country_date = []
    country_stat = [] 
    country_df[stat] = ""
    
    #creates new df to plot from full df
    for index, row in all_metrics_df.iterrows():
        if(country_name in index):
            country_date.append(index[1])
            country_stat.append(float(row[stat]))
    
    country_df['Date'] = country_date
    country_df['Date']= pd.to_datetime(country_df['Date']) 
    country_df.set_index('Date', inplace=True)
    country_df[stat] = country_stat
    
    country_df.plot(figsize=(10,5))
    
    
def outputCSV(df, path):
    df.to_csv(r''+path, index = False)
    
# set os path to delete old data folder
os_path = "path/to/copy"
os.chdir(os_path)

git_url = 'https://github.com/CSSEGISandData/COVID-19.git'

folder_name = "COVID19_REPO"
data_name = "COVID19_GlobalDaily"
csv_out = "COVID.csv"

data_path = ("path/to/copy/COVID19_REPO/" + 
    "csse_covid_19_data/csse_covid_19_daily_reports")

copy_data_path = "path/to/copy/COVID19_GlobalDaily"

deleteOld(os_path, folder_name, data_name)
cloneRepo(git_url, os_path, folder_name)
copyDaily(data_path, copy_data_path)
raw_df = mergeDF(copy_data_path)
grouped_df = groupbyCountry(raw_df)
plotMetric(grouped_df, 'US', 'Confirmed')
outputCSV(raw_df, os_path + csv_out)