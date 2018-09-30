# Module Only used for Clean Tokenizing of Twitter Data

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


def raw_to_tweet(raw_tweets=list(), na=None):
    '''
    :param raw_tweets: list -> Pass raw json tweets
    :param na: -> Future use
    :return tweets: -> Readable Tweets
    '''
    raw_tweets.extend(raw_tweets)
    tweets = [x.text for x in raw_tweets]
    tweets = [x.lower() for x in tweets]
    for tweet in range(len(tweets)):
        print(tweet, '. ', tweets[tweet])
    return tweets


def tokenize(tweet=str()):
    '''
    :param tweet: Single tweet
    :return: tokenzed with username mentions, hash tags, HTML tags, URLS,
    numbers, other words,
    '''
    return tokens_re.findall(tweet)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def dissolve_hashtag_puncs(s):
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
