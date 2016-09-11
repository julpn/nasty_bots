from mens_hate_speech import mens_bot, mens_reply
from gun_hate_speech import gun_bot, gun_reply
from lives_matter_hate_speech import lives_matter_bot, lives_matter_reply
from uncle_hate_speech import tweet_bot, uncle_reply

from threading import Thread

if __name__ == "__main__":
    # Hate speech
    m = Thread(target=mens_bot)
    m.start()
    g = Thread(target=gun_bot)
    g.start()
    l = Thread(target=lives_matter_bot)
    l.start()
    u = Thread(target=tweet_bot)
    u.start()

    # Reply bots
    mr = Thread(target=mens_reply)
    mr.start()
    gr = Thread(target=gun_reply)
    gr.start()
    lr = Thread(target=lives_matter_reply)
    lr.start()
    ur = Thread(target=uncle_reply)
    ur.start()