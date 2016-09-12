# -*- coding: utf-8 -*-

import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

from tweepy import API
from random import randint
import tweepy
import time

import logging

from apscheduler.schedulers.background import BackgroundScheduler

emojis = [u'\U0001F601',u'\U0001F602',u'\U0001F603',u'\U0001F604',u'\U0001F605',u'\U0001F606',u'\U0001F609',u'\U0001F60A',u'\U0001F60B',u'\U0001F60C',u'\U0001F60D',u'\U0001F60F',u'\U0001F612',u'\U0001F613',u'\U0001F614',u'\U0001F616',u'\U0001F618',u'\U0001F61A',u'\U0001F61C',u'\U0001F61D',u'\U0001F61E',u'\U0001F628',u'\U0001F629',u'\U0001F62A',u'\U0001F62B',u'\U0001F62D',u'\U0001F630',u'\U0001F631',u'\U0001F638',u'\U0001F639',u'\U0001F63A',u'\U0001F63B',u'\U0001F63C',u'\U0001F63D',u'\U0001F63F',u'\U0001F648',u'\U0001F649']
punc = ['.', '', '!', '!!', '!!!', '!!!', '-', '--']
sorrys = ['Hey, I thought about what you said last night and I am so sorry!', "Wow, I couldn't sleep night. You were right!",
          "Hey again, I keep thinking about our conversation. I was very rude.", "Hi there, last night was really rough. You were right",
          "I said some things I regret last night.", "I was up all night thinking about what you said. Wow."]

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

    def send_reply(self, text, id):
        print text
        self.twitterApi.update_status(status=text, in_reply_to_status_id=text)

    def on_data(self, data):
        tweet = json.loads(data.strip())

        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == self.user_id
        quote_tweet = tweet.get('target_object', {}).get('quoted_status',{}).get('user',{}).get('id_str')

        if not from_self and ((retweeted is not None and not retweeted) or quote_tweet):
            print "here"

            tweetId = tweet.get('id_str')
            if quote_tweet:
                screenName = tweet.get('target_object', {}).get('user',{}).get('screen_name')
            else:
                screenName = tweet.get('user',{}).get('screen_name')

            sorry = None
            if data.lower().find('compassion') > -1:
                chatResponse = 'fuck you libtard get fucked by ' + str(randint(5, 9000)) + ' dicks'
                sorry = '@' + screenName + ' ' + sorrys[randint(0, len(sorrys) - 1)] + str(randint(50,1000)) + ' apologies' + punc[randint(0, len(punc) - 1)] + emojis[randint(0, len(emojis) - 1)] + emojis[randint(0, len(emojis) - 1)]
            else:
                chatResponse = (self.lines[randint(0, self.num_lines - 1)]).replace('\n', '') + punc[randint(0, len(punc) - 1)] + emojis[randint(0, len(emojis) - 1)]

            replyText = '@' + screenName + ' ' + chatResponse

            if len(replyText) > 140:
                replyText = replyText[0:139] + '…'

            try:
                print replyText
                self.send_reply(replyText, tweetId)
                if sorry:
                    if len(sorry) > 140:
                        sorry = replyText[0:139] + '…'
                    time.sleep(5)
                    self.send_reply(sorry, tweetId)
            except tweepy.TweepError:
                pass


    def on_error(self, status):
        print status
