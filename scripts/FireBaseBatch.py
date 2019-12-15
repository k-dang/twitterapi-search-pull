import os
from os import path

from dotenv import load_dotenv
load_dotenv()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# local
from TwitterEngine import TwitterEngine

cred = credentials.Certificate(os.getenv("firebase_credentials_path"))
firebase_admin.initialize_app(cred, {
    'storageBucket': 'twitter-api-store.appspot.com'
})
bucket = storage.bucket()
blobs = bucket.list_blobs()
blob_names = [blob.name for blob in blobs]
# for blob in blob_names:
#     print(blob)

def FireBasePullAndUpdate(query):
    source_blob_name = f'{query}-dataset.csv'
    # hold dataset for updating and push back to firebase storage
    destination_file_name = f'scripts/intermediate/{source_blob_name}'

    # download the dataset if exists
    if source_blob_name in blob_names:
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        print('Blob {} downloaded to {}.'.format(
            source_blob_name,
            destination_file_name))

    # call twitter api and save to dataset
    twitterEngine = TwitterEngine(destination_file_name)
    terms = [query, f'#{query}']
    twitterEngine.batch_pull(terms)

    # upload and replace current dataset
    source_file_name = destination_file_name
    destination_blob_name = source_blob_name
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

    print('Deleting intermediate files')
    os.remove(destination_file_name)

if __name__ == "__main__":
    companies = ['Tesla', 'Microsoft']

    for company in companies:
        # print(company)
        FireBasePullAndUpdate(company)