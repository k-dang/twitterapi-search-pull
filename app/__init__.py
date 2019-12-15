import datetime
from datetime import timedelta
import os
from dotenv import load_dotenv
import json

# firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# flask
from flask import Flask
from flask import jsonify
from flask import request

# local
from app.Models.DataSetReader import DataSetReader

# load env
load_dotenv()

# setup firebase admin sdk
cred_dict = json.loads(os.getenv("firebase_credentials_json"))
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred, {
    'storageBucket': 'twitter-api-store.appspot.com'
})

# download dataset from firestore storage
bucket = storage.bucket()
source_blob_name = "dataset.csv"
blob = bucket.blob(source_blob_name)
destination_file_name = "app/dataset.csv"
blob.download_to_filename(destination_file_name)

# figure out if dataset re download is needed
# maybe switch to once per day instead of checking file diff if usage is too high
def check_cache():
    storage_blob = bucket.get_blob(source_blob_name)
    storage_blob_size = storage_blob.size

    local_blob_size = os.stat(destination_file_name).st_size

    if (local_blob_size != storage_blob_size):
        blob.download_to_filename(destination_file_name)

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # body content must contain date
    # {
    #   "date": "2019-11-21"
    # }
    # return single day sentiment
    @app.route('/api/tesla/sentiment/day', methods=['POST'])
    def get_sentiment():
        data = request.json

        tesla_twitter_set = DataSetReader(destination_file_name)
        tesla_twitter_set.drop_dups_add_sentiment()

        date = datetime.datetime.strptime(data['date'], '%Y-%m-%d').date()
        date_before = date + timedelta(days=1)

        after = data['date']
        before = date_before.strftime('%Y-%m-%d')
        avg_sentiment_day = tesla_twitter_set.get_sentiment_range(after, before)

        return jsonify({
            'sentiment': avg_sentiment_day
        })

    # body content must contain the range as
    # {
    #   "from": "2019-11-21"
    #   "to": "2019-11-29"
    # }
    # return list of sentiments, 1 for each day
    @app.route('/api/tesla/sentiment/range', methods=['POST'])
    def get_sentiment_range():
        data = request.json

        # check_cache()
        tesla_twitter_set = DataSetReader(destination_file_name)
        tesla_twitter_set.drop_dups_add_sentiment()

        filtered_df = tesla_twitter_set.get_filtered_df(data['from'], data['to'] + '23:59:59')
        result_df = filtered_df.groupby(['created_at_date']).mean()
        sentiment_df = result_df['sentiment']
        sentiment_df.index = sentiment_df.index.map(str)

        result = sentiment_df.to_dict()
        formatted_result = [{'date': key, 'sentiment': result[key]} for key in result]

        return jsonify({
            'sentiments': formatted_result
        })

    return app
