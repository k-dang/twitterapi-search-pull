from flask import Flask
from app.Models.DataSetReader import DataSetReader

app = Flask(__name__)

@app.route('/')
def hello_world():
    target_date = '2019-11-23'
    tesla_twitter_set = DataSetReader(f'./csv/{target_date}-dataset.csv')
    tesla_twitter_set.drop_dups_add_sentiment()
    b = tesla_twitter_set.get_sentiment()

    my_dict = {}
    my_dict[target_date] = b

    return my_dict