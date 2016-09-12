# -*- coding: utf-8 -*-
from tweepy import Stream

from gun_keys import consumer_key, consumer_secret, access_token, access_token_secret, user_id
from bot import poster
from reply import ReplyToTweet

mean_file = "gun_hate_tweets.txt"
nice_file = "gun_nice_tweets.txt"

def gun_bot():

    while True:
        f = open(mean_file)
        filetext = f.read()
        tweets = filetext.split('\n')
        poster(tweets, consumer_key, consumer_secret, access_token, access_token_secret)
    f.close()

def gun_reply():
    while True:
        try:
            streamListener = ReplyToTweet(consumer_key, consumer_secret, access_token, access_token_secret, user_id, nice_file)
            twitterStream = Stream(streamListener.auth, streamListener)
            twitterStream.userstream(_with='user')
        except:
            pass
        else:
            break