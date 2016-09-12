# -*- coding: utf-8 -*-

from tweepy import OAuthHandler
from tweepy import API
import tweepy
import time
from random import randint
from liberal_keys import consumer_key, consumer_secret, access_token, access_token_secret

def poster(tweets, consumer_key, consumer_secret, access_token, access_token_secret):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitterApi = API(auth)

    t = tweets[randint(0, len(tweets) - 1)]
    punc = ['.', '..', '!', '!!', ';', ';;', ' ', '', '#', '^', '*', '@', '/', '|', '?!']
    if len(t) > 138:
        t = t[:138]
    t += punc[randint(0, len(punc) - 1)]
    if len(t) > 140:
        t = t[:139] + '…'.decode('utf-8')

    try:
        twitterApi.update_status(status=t)
        time.sleep(randint(300, 600))
    except tweepy.TweepError:
        pass


def liberal_tweet(tweet):
    # Separate authentication for liberal bot
    lib_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    lib_auth.set_access_token(access_token, access_token_secret)
    lib_api = tweepy.API(lib_auth)
    lib_api.update_status(tweet)