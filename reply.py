# -*- coding: utf-8 -*-

import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

from tweepy import API
from random import randint
import tweepy
import time
from bot import liberal_tweet

import logging


from apscheduler.schedulers.background import BackgroundScheduler

emojis = [u'\U0001F601',u'\U0001F602',u'\U0001F603',u'\U0001F604',u'\U0001F605',u'\U0001F606',u'\U0001F609',u'\U0001F60A',u'\U0001F60B',u'\U0001F60C',u'\U0001F60D',u'\U0001F60F',u'\U0001F612',u'\U0001F613',u'\U0001F614',u'\U0001F616',u'\U0001F618',u'\U0001F61A',u'\U0001F61C',u'\U0001F61D',u'\U0001F61E',u'\U0001F628',u'\U0001F629',u'\U0001F62A',u'\U0001F62B',u'\U0001F62D',u'\U0001F630',u'\U0001F631',u'\U0001F638',u'\U0001F639',u'\U0001F63A',u'\U0001F63B',u'\U0001F63C',u'\U0001F63D',u'\U0001F63F',u'\U0001F648',u'\U0001F649']
happy_emojis = [u'\U0001F601',u'\U0001F602',u'\U0001F603',u'\U0001F604',u'\U0001F605',u'\U0001F606',u'\U0001F609',u'\U0001F60A',u'\U0001F60B',u'\U0001F60C',u'\U0001F60D',u'\U0001F63A',u'\U0001F63B',u'\U0001F63C',u'\U0001F63D',u'\U0001F63F',u'\U0001F648',u'\U0001F649']

punc = ['.', '', '!', '!!', '!!!', '!!!', '-', '--']
sorrys = ['Hey, I thought about what you said last night and I am so sorry!', "Wow, I couldn't sleep night. You were right!",
          "Hey again, I keep thinking about our conversation. I was very rude.", "Hi there, last night was really rough. You were right",
          "I said some things I regret last night.", "I was up all night thinking about what you said. Wow."]
prefixes = ["Wow."]

class ReplyToTweet(StreamListener):

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, user_id, file):

        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.twitterApi = API(self.auth)
        self.user_id = user_id

        logging.basicConfig()

        self.scheduler = BackgroundScheduler()

        f = open(file)
        self.lines = f.readlines()
        self.num_lines = 0
        for l in self.lines:
            self.num_lines += 1
        f.close()

    def clean_tweet(self, text, screename):
        text += punc[randint(0, len(punc) - 1)]
        if len(text) > 140:
            text = text[0:139] + '…'
        text = '@' + screename + ' ' + text
        return text

    def send_reply(self, text, id):
        self.twitterApi.update_status(status=text, in_reply_to_status_id=text)

    def on_data(self, data):
        tweet = json.loads(data.strip())

        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == self.user_id
        quote_tweet = tweet.get('target_object', {}).get('quoted_status',{}).get('user',{}).get('id_str')

        if not from_self and ((retweeted is not None and not retweeted) or quote_tweet):

            tweetId = tweet.get('id_str')
            if quote_tweet:
                screenName = tweet.get('target_object', {}).get('user',{}).get('screen_name')
            else:
                screenName = tweet.get('user',{}).get('screen_name')

            sorry = None
            if data.lower().find('compassion') > -1:
                chatResponse = 'fuck you libtard get fucked by ' + str(randint(5, 9000)) + ' dicks'
                sorry = self.clean_tweet(sorrys[randint(0, len(sorrys) - 1)] + str(randint(50,1000)) + ' apologies' + emojis[randint(0, len(emojis) - 1)] + emojis[randint(0, len(emojis) - 1)], screenName)
            else:
                chatResponse = (self.lines[randint(0, self.num_lines - 1)]).replace('\n', '') + emojis[randint(0, len(emojis) - 1)]

            replyText = self.clean_tweet(chatResponse, screenName)

            try:
                self.send_reply(replyText, tweetId)
                if sorry:
                    time.sleep(5)
                    self.send_reply(sorry, tweetId)
            except tweepy.TweepError:
                pass

            if quote_tweet == '774720778998874112' or tweet.get('in_reply_to_user_id_str') == '774720778998874112':
                f = open("liberal_tweets.txt")
                lib_lines = f.readlines()
                num_lib_lines = 0
                for l in lib_lines:
                    num_lib_lines += 1
                lib_tweet = self.clean_tweet(lib_lines[randint(1, num_lib_lines - 1)].replace('\n', '') + happy_emojis[randint(0, len(happy_emojis) - 1)] + happy_emojis[randint(0, len(happy_emojis) - 1)], screenName)

                liberal_tweet(lib_tweet)
                f.close()



    def on_error(self, status):
        print status
