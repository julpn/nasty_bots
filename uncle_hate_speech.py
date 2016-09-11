# -*- coding: utf-8 -*-

from uncle_keys import consumer_key, consumer_secret, access_token, access_token_secret
from tweet_maker import make_that_tweet
from bot import poster

def tweet_bot():
    while True:
        tweets = make_that_tweet()
        poster(tweets, consumer_key, consumer_secret, access_token, access_token_secret)

if __name__ == '__main__':
    tweet_bot()