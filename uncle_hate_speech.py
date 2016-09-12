# -*- coding: utf-8 -*-
from tweepy import Stream
import sys

from uncle_keys import consumer_key, consumer_secret, access_token, access_token_secret, user_id
from tweet_maker import make_that_tweet
from bot import poster
from reply import ReplyToTweet

nice_file = 'nice_tweets.txt'

def tweet_bot():
    while True:
        tweets = make_that_tweet()
        poster(tweets, consumer_key, consumer_secret, access_token, access_token_secret)

def uncle_reply():
    while True:
        try:
            streamListener = ReplyToTweet(consumer_key, consumer_secret, access_token, access_token_secret, user_id, nice_file)
            twitterStream = Stream(streamListener.auth, streamListener)
            twitterStream.userstream(_with='user')
        except:
            print sys.exc_info()[0]
            pass
        else:
            break