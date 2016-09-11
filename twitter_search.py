# -*- coding: utf-8 -*-

import base64
import requests
from uncle_keys import consumer_key, consumer_secret


def twitterpull(term):
    all_tweets = []

    base_url = 'https://api.twitter.com/1.1/'
    endpoint = 'search/tweets.json'

    bearer_token_credentials = base64.urlsafe_b64encode(
        '{}:{}'.format(consumer_key, consumer_secret).encode('ascii')).decode('ascii')
    url = 'https://api.twitter.com/oauth2/token'
    headers = {
        'Authorization': 'Basic {}'.format(bearer_token_credentials),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    data = 'grant_type=client_credentials'
    response = requests.post(url, headers=headers, data=data)
    response_data = response.json()

    if response_data['token_type'] == 'bearer':
        bearer_token = response_data['access_token']
    else:
        raise RuntimeError('unexpected token type: {}'.format(response_data['token_type']))

    max_id = 99999999999999999999999

    header = {"Authorization": "Bearer {}".format(bearer_token),
              'Accept-Encoding': 'gzip', }

    y = 0
    while y < 3:
        params = {"q": term,
              "count": 100,
              "exclude": "retweets",
              "max_id": max_id}

        r = requests.get(base_url + endpoint,
                             params=params,
                             headers=header)
        result = r.json()
        for t in result['statuses']:
            all_tweets.append((t['text']).replace('\t', ' ').replace('\n', ' ').replace('\r', ' '))
            max_id = t['id_str']
        y += 1

    return all_tweets