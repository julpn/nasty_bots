# -*- coding: utf-8 -*-
from tweepy import Stream

from mens_keys import consumer_key, consumer_secret, access_token, access_token_secret, screen_name, user_id
from bot import poster
from reply import ReplyToTweet

mean_file = "mens_hate_tweets.txt"
nice_file = "mens_nice_tweets.txt"

def mens_bot():

    while True:
        f = open(mean_file)
        filetext = f.read()
        tweets = filetext.split('\n')
        poster(tweets, consumer_key, consumer_secret, access_token, access_token_secret)
    f.close()

def mens_reply():
    streamListener = ReplyToTweet(consumer_key, consumer_secret, access_token, access_token_secret, user_id, nice_file)
    twitterStream = Stream(streamListener.auth, streamListener)
    twitterStream.userstream(_with='user')