from os import getenv

from certifi import where
from dotenv import load_dotenv
from MonsterLab import Monster
from pandas import DataFrame
from pymongo import MongoClient

from dotenv import load_dotenv
import os

# Load the environment variables from .env file
load_dotenv()


class Database:
     def __init__(self):
        # Connect to the MongoDB database
        self.client = MongoClient(getenv('MONGO_URI'))
        self.db = self.client['bandersnatch']  # Database name
        self.collection = self.db['monsters']  # Collection name

    def seed(self, amount):
        # This method will add `amount` of dummy data to the collection
        dummy_data = [{'name': f'Monster_{i}'} for i in range(amount)]
        self.collection.insert_many(dummy_data)

    def reset(self):
         # This method will delete all documents in the collection
        self.collection.delete_many({})

    def count(self) -> int:
        # This method returns the number of documents in the collection
        return self.collection.count_documents({})

    def dataframe(self) -> DataFrame:
        # This method returns all documents in the collection as a pandas DataFrame
        data = list(self.collection.find({}, {'_id': False}))
        return DataFrame(data)

    def html_table(self) -> str:
        # This method returns an HTML table representation of the DataFrame
        df = self.dataframe()
        return df.to_html() if not df.empty else None