import os
from os import path

from dotenv import load_dotenv
load_dotenv()

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

import pandas as pd

cred = credentials.Certificate(os.getenv("firebase_credentials_path"))
firebase_admin.initialize_app(cred, {
    'storageBucket': 'twitter-api-store.appspot.com'
})
bucket = storage.bucket()
blobs = bucket.list_blobs()
# blob_names = [blob.name for blob in blobs]

for blob in blobs:
    destination_file_name = f'scripts/intermediate/{blob.name}'
    blob.download_to_filename(destination_file_name)
    print('Blob {} downloaded to {}.'.format(
            blob.name,
            destination_file_name))
    df = pd.read_csv(destination_file_name)
    print(df.shape)

    df = df.drop_duplicates(subset='id', keep='first')
    print(df.shape)

    df.to_csv(destination_file_name, index = None, header=True)
    blob.upload_from_filename(destination_file_name)
    print('Deleting intermediate files')
    os.remove(destination_file_name)
# need to remove dups