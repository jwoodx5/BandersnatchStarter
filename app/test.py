from os import getenv
from dotenv import load_dotenv
from typing import Optional, Dict
from pymongo import MongoClient, errors
from certifi import where
from pandas import DataFrame
from MonsterLab import Monster  

class Database:
    """
    Database class for managing MongoDB operations.
    It allows seeding the database with default data,
    resetting the database, counting documents, and converting the data to
    a pandas DataFrame or an HTML table.
    """
 
    def __init__(self, collection: str):
        """
        Initialize the Database with the specified MongoDB collection.
        """
        load_dotenv()  # Load the environment variables from .env file
        try:
            # Establish connection to MongoDB
            self.client = MongoClient(getenv("MONGO_URL"), tlsCAFile=where())
            self.database = self.client['Database']
            self.collection = self.database[collection]
        except errors.ConnectionError as e:
            print(f"Error connecting to MongoDB: {e}")
            raise ConnectionError("Could not connect to MongoDB") from e

    def seed(self, amount=1500) -> bool:
        """
        Seed the database with a given amount of Monster data.
        """
        try:
            data = [Monster().to_dict() for _ in range(amount)]
            result = self.collection.insert_many(data)
            return result.acknowledged
        except errors.BulkWriteError as e:
            print(f"Error seeding data: {e}")
            return False

    def reset(self) -> dict:
        """
        Reset the database by deleting all documents within the collection.
        """
        try:
            return self.collection.delete_many({}).raw_result
        except errors.OperationFailure as e:
            print(f"Error resetting the database: {e}")
            raise

    def count(self) -> int:
        """
        Count the number of documents in the collection.
        """
        try:
            return self.collection.count_documents({})
        except errors.PyMongoError as e:
            print(f"Error counting documents: {e}")
            raise

    def dataframe(self, query: Optional[Dict] = None) -> DataFrame:
        """
        Convert the documents in the collection to a pandas DataFrame.
        """
        try:
            documents = list(self.collection.find(query or {}, {'_id': False}))
            return DataFrame(documents)
        except Exception as e:
            print(f"Error fetching or converting data: {e}")
            raise

    def html_table(self) -> str:
        """
        Convert the collection's data to an HTML table.
        """
        try:
            df = self.dataframe()
            return df.to_html()
        except Exception as e:
            print(f"Error converting data to HTML table: {e}")
            raise

    def save_function(self, func_name: str, js_code: str):
        """
        Save a JavaScript function in MongoDB.
        """
        try:
            return self.database.system.js.save({
                "_id": func_name,
                "value": self.database.eval(f"function() {{ {js_code} }}")
            })
        except errors.OperationFailure as e:
            print(f"Error saving JavaScript function: {e}")
            raise

    def delete_function(self, func_name: str):
        """
        Delete a JavaScript function from MongoDB.
        """
        try:
            return self.database.system.js.delete_one({"_id": func_name})
        except errors.OperationFailure as e:
            print(f"Error deleting JavaScript function: {e}")
            raise

    if __name__ == '__main__':
        APP.run(debug=True)  