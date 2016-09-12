# -*- coding: utf-8 -*-
from tweepy import Stream

from lives_matter_keys import consumer_key, consumer_secret, access_token, access_token_secret, user_id
from bot import poster
from reply import ReplyToTweet

mean_file = "lives_matter_hate_tweets.txt"
nice_file = "lives_matter_nice_tweets.txt"

def lives_matter_bot():

    while True:
        f = open("lives_matter_hate_tweets.txt")
        filetext = f.read()
        tweets = filetext.split('\n')
        poster(tweets, consumer_key, consumer_secret, access_token, access_token_secret)
    f.close()

def lives_matter_reply():
    while True:
        try:
            streamListener = ReplyToTweet(consumer_key, consumer_secret, access_token, access_token_secret, user_id, nice_file)
            twitterStream = Stream(streamListener.auth, streamListener)
            twitterStream.userstream(_with='user')
        except:
            pass
        else:
            break