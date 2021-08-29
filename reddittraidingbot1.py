import praw
import config
from textblob import TextBlob
from binance.client import Client
from binance.enums import *

client = Client(config.BINANCE_KEY, config.BINANCE_KEY)
info = client.get_account()
print((info))

reddit = praw.Reddit(
    client_id=config.REDDIT_ID,
    client_secret=config.REDDIT_SECRET,
    password=config.REDDIT_PASS,
    user_agent="USERAGENT",
    username=config.REDDIT_USER,

)
lst = []
neededSentiments = 3
TRADE_SYMBOL = 'BTCUSDT'
TRADE_QUANTITY = 0.000010
in_position = False


def Average(lst):
    if len(lst) == 0:
        return len(lst)
    else:
        return sum(lst[-neededSentiments:]) / neededSentiments


def order(order, side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print('sending order')
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print("As exception is occured: " + e)
        return False
    return True


# print(reddit)
# for submission in reddit.subreddit("bitcoin").hot(limit=25):
#     print(submission.title)
# for comment in reddit.subreddit("wallstreetbeets").stream.comments():
# for comment in reddit.subreddit("nio").stream.comments():
for comment in reddit.subreddit("bitcoinmarkets").stream.comments():
    redditComment = comment.body
    blob = TextBlob(redditComment)
    sent = blob.sentiment

    print(redditComment)

    print(" ********** Sentiment is " + str(sent.polarity))

    if sent.polarity != 0.0:
        lst.append(sent.polarity)
        avg = round(Average(lst), 2)
        print(" ********** Total Sentiment is currently: " + str(round(Average(lst), 4)) + " and there are " + str(
            len(lst)) + " elements")


        if round(Average(lst)) > 0.1 and len(lst) > neededSentiments:
            if in_position:
                print(" ********** BUY ORDER, BUT WE OWN  **********")
            else:
                print(" ********** BUY ORDER **********")
                order_succedded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succedded:
                    in_position = True
        elif round(Average(lst)) < -0.1 and len(lst) > neededSentiments:
            if in_position:
                order_succedded = "SELL IT!!!"
                order_succedded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                if order_succedded:
                    in_position = False
            else:
                print(" ********** SELL ORDER, BUT WE DON'T  OWN  **********")
