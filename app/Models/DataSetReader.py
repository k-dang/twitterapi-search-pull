import pandas as pd
from textblob import TextBlob

class DataSetReader():
    def __init__(self, csv_file_name):
        self.df = pd.read_csv(csv_file_name)

    def drop_duplicates(self):
        self.sort_by_popular()
        self.df = self.df.drop_duplicates(subset='id', keep='first')

    def add_sentiment(self):
        self.df['sentiment'] = self.df.apply(lambda row: self.__get_sentiment(row), axis=1)

    def __get_sentiment(self, row):
        analysis = TextBlob(str(row['text']))
        return analysis.sentiment.polarity

    def sort_by_popular(self):
        self.df = self.df.sort_values(by=['retweet_count', 'favorite_count', 'id'], ascending=False)

    # returns the average sentiment for the df
    def get_sentiment(self):
        return self.df['sentiment'].mean()

    def get_sentiment_range(self, after, before):
        filter_date_after = self.df['created_at'] > after
        filter_date_before = self.df['created_at'] < before
        df_date_filter = self.df[filter_date_after & filter_date_before]
        return df_date_filter['sentiment'].mean()

    def drop_dups_add_sentiment(self):
        self.drop_duplicates()
        self.add_sentiment()

    def get_df(self):
        return self.df


if __name__ == "__main__":
    target_date = '2019-11-23'
    tesla_twitter_set = DataSetReader(f'./csv/{target_date}-dataset.csv')
    tesla_twitter_set.drop_dups_add_sentiment()

    # after = '2019-11-20 00:00:00'
    # before = '2019-11-22 00:00:00'
    # a = tesla_twitter_set.get_sentiment_range(after, before)
    # print(a)

    b = tesla_twitter_set.get_sentiment()
    print(b)

    target_date = '2019-11-24'
    tesla_twitter_set = DataSetReader(f'./csv/{target_date}-dataset.csv')
    tesla_twitter_set.drop_dups_add_sentiment()
    b = tesla_twitter_set.get_sentiment()
    print(b)
