import tweepy
from tweepy import OAuthHandler
import tweety_nltk as tnltk

# Consumer API Keys
consumer_key = "your API KEY"
consumer_secret = "your API SECRET KEY"

# Consumer Access Keys
access_key = "your CONSUMER KEY"
access_secret = "your CONSUMER SECRET"

# Authorize this Python Script
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

# Access API
api = tweepy.API(auth) # api object is now your access point

# Let's read out own timeline:
no=1
for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print("S",no, status.text)
    no+=1

no=1
# Fetch Friends
for friends in tweepy.Cursor(api.friends).items(5):
    # Following
    print("F",no, friends._json.get('name'))
    no+=1

# Fetch Your Followers
for follower in tweepy.Cursor(api.followers).items(5):
    print(follower._json.get('name'))

# Fetch Tweets of any user
user_name = str(input("Enter Twitter Handle Name:"))
no_of_twt = int(input("Enter No. of tweets to fetch:"))

# Begin Fetching
alltweets = [] # Empty list to store Semi-Processed Tweets
raw_tweets = api.user_timeline(screen_name='tejasprawal', count=4)
tweets = tnltk.raw_to_tweet(raw_tweets)

# TOKENIZING
from nltk.tokenize import word_tokenize
# print(word_tokenize(tweets[0]))

clean_tweets = []
for tweet in tweets:
    tok_twt = tnltk.preprocess(tweet)
    cleaned_twt = tnltk.remove_usernames(tok_twt)
    cleaned_twt = tnltk.remove_links(cleaned_twt)
    cleaned_twt = tnltk.dissolve_hashtag_puncs(cleaned_twt)
    clean_tweets.append(cleaned_twt)
print('_______________CLEANED\n',clean_tweets)

# Create a CSV File
with open('tweets.csv', 'wb') as f:
    for one_tweet in clean_tweets:
        print(' '.join(one_tweet) + ',')
        sentence = ' '.join(one_tweet) + ',\n'
        f.write(str.encode(sentence))

f.close()

import pandas as pd
data = pd.read_csv('tweets.csv', header=None)
data.columns = ['tweets', 'sentiment']
tweet_impact = pd.DataFrame(columns=['tweets', 'positive'])

#  ____  _____ _   _ _____ ___ __  __ _____ _   _ _____
# / ___|| ____| \ | |_   _|_ _|  \/  | ____| \ | |_   _|
# \___ \|  _| |  \| | | |  | || |\/| |  _| |  \| | | |
#  ___) | |___| |\  | | |  | || |  | | |___| |\  | | |
# |____/|_____|_| \_| |_| |___|_|  |_|_____|_| \_| |_|
# Analysis

import re
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

# Creating a Corpus
corpus = []
for i in range(0, data.__len__()):
    single_tweet = re.sub('[^a-zA-Z]', ' ', data['tweets'][i])
    single_tweet = single_tweet.lower()
    single_tweet = single_tweet.split()

    ps = PorterStemmer()
    nl = WordNetLemmatizer()
    single_tweet = [ps.stem(nl.lemmatize(word, pos='v')) for word in single_tweet if not word in set(stopwords.words('english'))]
    single_tweet = ' '.join(single_tweet)
    corpus.append(single_tweet)

from nltk.sentiment.vader import SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()
for twt in corpus:
    one_sentence = twt
    scores = sia.polarity_scores(one_sentence)
    print(one_sentence[:15] + '...',scores)

    POS = scores.get('pos')
    NEG = scores.get('neg')
    NEU = scores.get('neu')
    RES = str()

    if POS > NEG:
        RES = 1
    elif NEG > POS:
        RES = 0
    elif NEU >= 0.5 or POS > NEU:
        RES = 1
    elif NEU < 0.5:
        RES = 0

    tweet_impact = tweet_impact.append({'tweets':one_sentence, 'positive':RES}, ignore_index=True)
