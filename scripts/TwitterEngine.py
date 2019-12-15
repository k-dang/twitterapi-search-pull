import tweepy
import os
from os import path
import json
import csv
import re
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
load_dotenv()

class TwitterEngine():
    def __init__(self, csv_file_name):
        auth = tweepy.OAuthHandler(os.getenv("consumer_api_key"), os.getenv("consumer_api_secret_key"))
        self.api = tweepy.API(auth)
        self.csv_file_name = csv_file_name
        self.tweets_dict = {}
        self.row_header = "id,created_at,search_term,text,retweet_count,favorite_count\n"

    def __clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def __search_and_pull_tweets(self, term):
        for tweet in tweepy.Cursor(self.api.search, q=term, result_type='popular').items():
            row = [tweet.id, tweet.created_at, term, self.__clean_tweet(tweet.text), tweet.retweet_count, tweet.favorite_count]
            
            # write to one file
            self.__write_to_onefile(row)

            # save to dict which will eventuall write to multiple files
            # formatted_date = str(tweet.created_at.date());
            # if formatted_date in self.tweets_dict:
            #     tweetList = self.tweets_dict[formatted_date]
            #     tweetList.append(row)
            #     self.tweets_dict[formatted_date] = tweetList
            # else:
            #     self.tweets_dict[formatted_date] = [row]

    def __file_exists(self, file):
        return path.exists(file)

    # Accepts a list of terms to look up
    def batch_pull(self, terms):
        for term in terms:
            self.__search_and_pull_tweets(term)
        
        # write to multiple files
        if bool(self.tweets_dict):
            for key in self.tweets_dict:
                file_path = f'../csv/{key}-{self.csv_file_name}'
                if (self.__file_exists(key)):
                    with open(file_path, 'a') as f:
                        writer = csv.writer(f)
                        writer.writerows(self.tweets_dict[key])
                else:
                    with open(file_path, 'w+') as f:
                        f.write(self.row_header)
                        writer = csv.writer(f)
                        writer.writerows(self.tweets_dict[key])

    # do I need to create a function to pull into one file?
    def __write_to_onefile(self, row):
        file_path = f'{self.csv_file_name}'
        if (self.__file_exists(file_path)):
            with open(file_path, 'a') as f:
                writer = csv.writer(f)
                writer.writerow(row)
        else:
            with open(file_path, 'w+') as f:
                f.write(self.row_header)
                writer = csv.writer(f)
                writer.writerow(row)

