import tweepy
from tweepy import OAuthHandler
import pdb

# Consumer API Keys
consumer_key = "aooIhU174fTBCddpIvGeoNuIk"
consumer_secret = "VqxjnAJDk1GBupsNePcC19H4wap9mOt4avP50QcPBQw2Gt0k1m"

# Consumer Access Keys
access_key = "617869654-hz5AiU1kO9YBohzPvAflQgkIJHaZoPUJCKvv6CWW"
access_secret = "tevOCPoyrgFtEMoFUJo7mWvcArwnQAYrMS8t6zng89s0v"

# Authorize this Python Script
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Access API
api = tweepy.API(auth) # api object is now your access point
#
# # Let's read out own timeline:
# no=1
# for status in tweepy.Cursor(api.home_timeline).items(10):
#     # Process a single status
#     print("S",no, status.text)
#     no+=1
#
# no=1
# # Fetch Friends
# for friends in tweepy.Cursor(api.friends).items(5):
#     # Following
#     print("F",no, friends._json.get('name'))
#     no+=1

# # Fetch Your Followers
# for follower in tweepy.Cursor(api.followers).items(5):
#     print(follower._json.get('name'))

# Fetch Tweets of any user
# user_name = str(input("Enter Twitter Handle Name:"))
# no_of_twt = int(input("Enter No. of tweets to fetch:"))

# Begin Fetching
alltweets = [] # Empty list to store Semi-Processed Tweets
raw_tweets = api.user_timeline(screen_name='tejasprawal', count=4)
alltweets.extend(raw_tweets)
tweets = [x.text for x in alltweets]
tweets = [x.lower() for x in tweets]
for tweet in range(len(tweets)):
    print(tweet, '. ', tweets[tweet])

# TOKENIZING
from nltk.tokenize import word_tokenize
# print(word_tokenize(tweets[0]))
# tweepy.Cursor(api.send_direct_message('Tejas', 'tejasprawal', '617869654', 'Hello'))

# CLEANING
import re
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def remove_hashtag_puncs(s):
    no_hash = []
    clean_txt = []
    #pdb.set_trace()
    for i, word in enumerate(s):
        if word.startswith('#'):
            no_hash.append(word.split('#')[1])
        elif word not in ['.', ',', '…', ':']:
            clean_txt.append(word)
    return clean_txt+no_hash


def remove_links(s):
    for i, word in enumerate(s):
        if word.startswith('http'):
            s.pop(i)
    return s

def remove_usernames(s):
    for i, word in enumerate(s):
        if word.startswith('@'):
            s.pop(i)
    return s


clean_tweets = []
for tweet in tweets:
    tok_twt = preprocess(tweet)
    cleaned_twt = remove_usernames(tok_twt)
    cleaned_twt = remove_links(cleaned_twt)
    cleaned_twt = remove_hashtag_puncs(cleaned_twt)
    clean_tweets.append(cleaned_twt)
print('_______________CLEANED\n',clean_tweets)

# Create text file
with open('tweets.csv', 'wb') as f:
    for t in clean_tweets:
        print(' '.join(t)+',')
        sentence = ' '.join(t) + ',\n'
        f.write(str.encode(sentence))

f.close()

import pandas as pd
data = pd.read_csv('tweets.csv', header=None)
data.columns = ['tweets', 'sentiment']

df = pd.DataFrame(columns=['tweets', 'sentiment'])

for t in clean_tweets:
    print(' '.join(t) + ',')
    data.append({'tweets':' '.join(t),}, ignore_index=True)
