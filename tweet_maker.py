from random import randint, shuffle
from twitter_search import twitterpull


def rand(arr):
    return randint(0, len(arr) - 1)

def replace_link(text, location):
    return text[:location] + text[len(text) - location + 24]

def make_that_tweet():
    results = []
    terms = ['obummer', 'sjw', 'cuck', 'feminazi']
    a_parts = []
    b_parts = []
    for term in terms:
        raw = twitterpull(term)
        x = 0
        for text in raw:
            pos = text.lower().find(term)
            if pos < 50 or pos > len(text) - 50 or text.find('@') > -1 or text.find('ass') > -1:
                pass
            else:
                a_parts.append(text[:pos])
                b_parts.append(text[pos:len(text)])

    while x < len(a_parts):
        a_rand = rand(a_parts)
        b_rand = rand(b_parts)
        text = a_parts[a_rand] + b_parts[b_rand]
        a_parts.pop(a_rand)
        b_parts.pop(b_rand)
        place = text.find('http')
        while place > -1:
            try:
                text = replace_link(text, place)
                place = text.find('http')
            except IndexError:
                place = 0
                pass
        results.append(text)
        x += 1

    shuffle(results)
    return results
