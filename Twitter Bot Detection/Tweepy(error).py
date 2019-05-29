# -*- coding: utf-8 -*-
"""
Created on Sun Dec 02 11:34:02 2018

@author: Himanshu
"""

import tweepy
import os,sys, csv, time
import pandas as pd
import numpy as np

print ("Gathering real-time data from Twitter...")
start=time.time()
#Twitter credentials
consumer_key='5l13crF9Wjmyc4XFCtiscVCug'
consumer_secret='XLH5WteBamDSQxgf3T9ejmhnc7Ys76fyp5vuAJAXTnS3A8ch0x'
access_key = '894694105-nPCgnlhSffrXUZOP3xAFWR6Il1X8ugzRlrMFVYIC'
access_secret = 'MZU8wVtfPq10HLmsYjNDiDXTxiQXkQhjjJPVKVndlEEo4'

def createOutput(data, isbot):
    header = ['id', 'id_str', 'screen_name', 'location', 'description', 'url',
                'followers_count', 'friends_count', 'listed_count', 'created_at',
                'favourites_count', 'verified', 'statuses_count', 'lang', 'status',
                'default_profile','default_profile_image', 'has_extended_profile',
                'name']
    d = {}
    for key in header:
        if key not in data.keys():
            d[key] = ""
        elif key == 'status':
            d[key] = str(data[key])
        else:
            d[key] = data[key]

    df = pd.DataFrame(d, columns= header, index=np.arange(1))
    df['bot'] = isbot
    return df

def get_bots_list():
    bots_list = []
    for bots in tweepy.Cursor(api.list_members, '01101O10', 'bot-list').items():
        bots_list.append (bots._json['screen_name'])
    return bots_list[:50]

def real_users_list():
    real_users = []
    for users in tweepy.Cursor(api.list_members, 'Scobleizer', 'most-influential-in-tech').items():
        real_users.append (users._json['screen_name'])
    return real_users[:50]

def get_user_list():
    user_list = get_bots_list() + real_users_list()
    filename = 'bots_nonbots_output2.csv'
    return user_list, filename

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key,access_secret)
api = tweepy.API(auth)

user_list, filename = get_user_list()

df = pd.DataFrame()
for i,users in enumerate(user_list, start=1):
    isbot=0
    if(i<=50):
        isbot=1
    data = api.get_user(users)._json
    data_df1 = createOutput(data, isbot)
    df = pd.concat([data_df1, df], axis= 0, ignore_index = True)

df.to_csv(filename, encoding='utf-8')
print ("Done. All records are saved to csv. \nDuration: "+str(time.time()-start)+" seconds.")