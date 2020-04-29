#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 09:59:26 2020

@author: brento

Takes a csv file formatted from the Twitter API
and runs sentiment analysis on it to determine the 
poliarity. Uses TextBlob library.
"""
from textblob import TextBlob
import pandas as pd

# path to csv
data = pd.read_csv("twitter.csv")

def sentiment(tweet):
    analysis = TextBlob(tweet)
    return analysis.sentiment.polarity
    
data['text'] = data['text'].astype(str)
sent = []
for i in range(0,len(data)):
    sent.append(sentiment(data['text'][i]))

data['sentiment'] = sent

data['created_at'] = data['created_at'].astype(str)

dates = []
for i in range(0,len(data)):
    dates.append((data['created_at'][i].split(' ')[0]))
    
data['created_at'] = dates

path = "/Users/brento/Desktop/twitter.csv"
data.to_csv(r''+path, index = False)

# groupby date

group_confirmed = data.groupby(['created_at']).agg({'sentiment': ['sum']})
group_confirmed['Date'] = group_confirmed.index
agg_path = "/Users/brento/Desktop/agg_twitter.csv"
group_confirmed.to_csv(r''+agg_path, index = True)
