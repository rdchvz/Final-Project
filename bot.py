# Create a Reddit bot to moderator a subreddit that keeps track of the top 10 talked about stocks on reddit and releases a report every monday.

import praw
import requests
import time
import pprint
import re
import datetime
import math

now = datetime.datetime.now() 

now_epoch = math.ceil(now.timestamp())
week_ago = now - datetime.timedelta(days=7)
week_ago_epoch = math.ceil(week_ago.timestamp())

reddit = praw.Reddit(client_id='_QpxqjHvL9MIdSqGTr6VFw', client_secret='_sDXmg_vzkPmr5xDW1Okv71TsV2d6A', user_agent='popularstonkbot', username="PopularStonkFinder", password="$HyunMin$",)
subreddit = reddit.subreddit("PopularStonkBot")


epoch_time = int(time.time())
data = requests.get(f"https://api.pushshift.io/reddit/submission/search/?after={week_ago_epoch}&before={now_epoch}&sort_type=score&sort=desc&subreddit=PopularStonkBot")

data = data.json()
tickers = []

popular = {}

for post in data["data"]:
    for ticker in re.findall(r'[$][A-Za-z][\S]*', post['selftext']):
        tickers.append(ticker)

for ticker in tickers:
    if ticker in popular:
        popular[ticker] += 1
    else:
        popular[ticker] = 1

sorted_dict = {}
for ticker in sorted(popular, key=popular.get, reverse=True):
    sorted_dict[ticker] = popular[ticker]

sorted_dict_keys = []

for ticker_key in sorted_dict.keys():
    sorted_dict_keys.append(ticker_key)

print(sorted_dict_keys)

post_text = f"""
Here are the top three tickers of the week from PopularStonkBot
{sorted_dict_keys[0]} : was mentioned {sorted_dict[sorted_dict_keys[0]]} times.
{sorted_dict_keys[1]} : was mentioned {sorted_dict[sorted_dict_keys[1]]} times.
{sorted_dict_keys[2]} : was mentioned {sorted_dict[sorted_dict_keys[2]]} times.
"""

subreddit.submit(title='Tickers of the week', selftext=post_text)


