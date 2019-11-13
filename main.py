import tweepy
import os
import json
import csv
import re
from dotenv import load_dotenv
load_dotenv()

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def search_and_pull_tweets(api, writer, term):
    for tweet in tweepy.Cursor(api.search, q=term, result_type='popular').items():
        row = [tweet.id, tweet.created_at, term, clean_tweet(tweet.text), tweet.retweet_count, tweet.favorite_count]
        writer.writerow(row)
    # print(tweet.user.name)

auth = tweepy.OAuthHandler(
    os.getenv("consumer_api_key"), os.getenv("consumer_api_secret_key"))

api = tweepy.API(auth)

f = open("dataset.csv", "a")
writer = csv.writer(f)
# f.write("id,created_at,text,retweet_count,favorite_count")

terms = ['Tesla', '#Tesla']

for term in terms:
    search_and_pull_tweets(api, writer, term)

f.close()
