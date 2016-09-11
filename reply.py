# -*- coding: utf-8 -*-

import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

from tweepy import API
from random import randint

import logging

from apscheduler.schedulers.background import BackgroundScheduler


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
        self.twitterApi.update_status(status=text, in_reply_to_status_id=text)

    def on_data(self, data):
        print data
        tweet = json.loads(data.strip())

        retweeted = tweet.get('retweeted')
        from_self = tweet.get('user',{}).get('id_str','') == self.user_id

        if retweeted is not None and not retweeted and not from_self:

            tweetId = tweet.get('id_str')
            screenName = tweet.get('user',{}).get('screen_name')
            tweetText = tweet.get('text')

            if data.lower().find('compassion') > -1:
                chatResponse = 'fuck you libtard' + str(randint(0, 900))

                self.scheduler.add_job(self.send_reply, 'interval', args=[":-(", tweetId], seconds=60)
                self.scheduler.start()
            else:
                chatResponse = self.lines[randint(0, self.num_lines - 1)] + str(randint(0, 900))

            replyText = '@' + screenName + ' ' + chatResponse

            if len(replyText) > 140:
                replyText = replyText[0:139] + '…'

            print('Tweet ID: ' + tweetId)
            print('From: ' + screenName)
            print('Tweet Text: ' + tweetText)
            print('Reply Text: ' + replyText)

            self.send_reply(replyText, tweetId)

    def on_error(self, status):
        print status
