# -*- coding: utf-8 -*-
"""Sentimental_Analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RkzWUVFBY1fVNN2mt5H9x_bKobQLFAGv
"""

import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import textblob
import re
from PIL import Image
import  streamlit as st
from Crypto_Dashboard import crypto_name


api_key='F6Hq8W2hScamTAiDbC8mkiSJY'
api_key_secret='fgQUE1yX5j1aGUkbv9v76NcqCHt6RywE6gz0px8aXeJOMQsRGR'
access_token='918824619007545345-wDZ5P7GEZMcuXCf8hS3XB2ouVjBIaVT'
access_token_secret='lgAaydyole1RrGf2ZgKzW9oRTLnF2QjWame6jH9ATYlf4'


authenticator=tweepy.OAuthHandler(api_key,api_key_secret)
authenticator.set_access_token(access_token,access_token_secret)

api=tweepy.API(authenticator,wait_on_rate_limit=True)
def senti(sym):
    crypt=sym
    search=f'#{crypt} -filter:retweets'
    tweet_cursor=tweepy.Cursor(api.search_tweets,q=search,lang='en',tweet_mode='extended').items(100)
    tweets=[tweet.full_text for tweet in tweet_cursor]
    tweets_df=pd.DataFrame(tweets,columns=['Tweets'])

    for _, row in tweets_df.iterrows():
        row['Tweets']=re.sub('http\S+','',row['Tweets'])
        row['Tweets']=re.sub('#\S+','',row['Tweets'])
        row['Tweets']=re.sub('@\S+','',row['Tweets'])
        row['Tweets']=re.sub('\\n','',row['Tweets'])

    tweets_df['Polarity']=tweets_df['Tweets'].map(lambda  tweet:textblob.TextBlob(tweet).sentiment.polarity)
    tweets_df['Result']=tweets_df['Polarity'].map(lambda pol: '+' if pol>0 else '-')

    positive=tweets_df[tweets_df.Result=='+'].count()['Tweets']
    negative=tweets_df[tweets_df.Result=='-'].count()['Tweets']

    plt.bar([0,1],[positive,negative],label=['Positive','Negative'],color=['green','red'])
    plt.legend()
#plt.show()
    plt.savefig('books_read.png')
    image1 = Image.open("books_read.png")
    st.header("**TWITTER NEWS SENTIMENTAL ANALYSIS**")

    st.write("The cryptocurrency market is largely driven by speculation."
         " Whether you agree with that statement or not is up to you, "
         "however many of the top traders in the space understand the importance of monitoring "
         "how the market is feeling (eg. @kazonomics on Twitter). Are you buying when everyone is happy "
         "and greedy, or when the salt levels are high? Again, I suggest you answer that on your own or look "
         "at quotes from Warren Buffet to understand the answer to that.")
    st.header("**Do you trade the news?**")
    st.write("If you’re a cryptocurrency trader, you’ve probably traded the news at least a few times. "
         "I know I did, with various degrees of success. The issue I noticed with this strategy is that, "
         "more often than not, by the time you become aware of a big piece of news for any given cryptocurrency, "
         "there are many other players who capitalised on the news, opened positions and made their moves. "
         "So unless you’re constantly checking for them, you won’t make the best possible trade. ")
    st.image(image1, use_column_width=True)
    cols=st.column(2)
    cols[0].header("Positive News")
    cols[0].write(positive)
    cols[1].header("Negative News")
    cols[1].write(negative)
