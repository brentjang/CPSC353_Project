#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 12:25:41 2020

@author: brento

Uses Twitter API to pull data and format to csv output.
"""

import tweepy as tw
import pandas as pd
import time
from datetime import date, timedelta

consumer_key= 'CONSUMER_KEY'
consumer_secret= 'CONSUMER_SECRET'
access_token= 'ACCESS_TOKEN'
access_token_secret= 'ACCESS_TOKEN_SECRET'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

end = date.today()
start = date(2020, 1, 22)

delta = end - start

date_range = []
for i in range(delta.days):
    day = start + timedelta(days=i)
    date_range.append(day)

# Define the search term and the date_since date as variables
search_words = "Asian" + " -filter:replies" + " -filter:retweets" 
date_since = ""

tweet_text = pd.DataFrame(columns=['created_at', 'id', 'text','retweet_count',
                             'favorite_count','user', 'location'])

# Collect tweets
    
for day in date_range:
    tweets = tw.Cursor(api.search,
                  q=search_words,
                  lang="en",
                  since=str(day)).items()
    print([[tweet.created_at] for tweet in tweets])
    while True:
        try:
            tweet = tweets.next()
            hi = [tweet.created_at, tweet.id, tweet.text, tweet.retweet_count,
                  tweet.favorite_count, tweet.user.screen_name, tweet.user.location]
            tweet_text = tweet_text.append(hi)
        except tw.TweepError:
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break
    
# Iterate and print tweets
# hi = [[tweet.created_at] for tweet in tweets]

