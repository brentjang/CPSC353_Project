#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 20:35:16 2020

@author: brento

Using GetOldTweets3, pulls data from Twitter based on search query
and compiles into a csv output.
"""

import GetOldTweets3 as got
import pandas as pd
from datetime import date, timedelta
import time

end = date.today()
start = date(2020, 1, 22)

delta = end - start

date_range = []
for i in range(delta.days):
    day = start + timedelta(days=i)
    date_range.append(day)


tweet_full = pd.DataFrame(columns=['created_at', 'id', 'text','retweet_count',
                                   'favorite_count','user', 'location'])

for i in range(0, len(date_range)-1):
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch("Asian")\
                                               .setSince(str(date_range[i]))\
                                               .setUntil(str(date_range[i+1]))\
                                               .setMaxTweets(1000)
    list_tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    
    for tweet in list_tweets:
        data = {'created_at':[tweet.date], 
                'id':[tweet.id], 
                'text':[tweet.text], 
                'retweet_count':[tweet.retweets],
                'favorite_count':[tweet.favorites], 
                'user':[tweet.username], 
                'location':[tweet.geo]}
        new_df = pd.DataFrame(data)
        tweet_full = tweet_full.append(new_df)
    
    time.sleep(60 * 5)
    
path = "/Users/brento/Desktop/twitter.csv"
tweet_full.to_csv(r''+path, index = False)
