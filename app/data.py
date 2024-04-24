from os import getenv, path
from typing import Optional, Dict
from pymongo import MongoClient
from dotenv import load_dotenv
from MonsterLab import Monster
from certifi import where
from pandas import DataFrame

class Database:
    """
    Database class for managing the MongoDB operations.
    It allows seeding the database with default data,
    resetting the database, counting documents, and converting the data to
    a pandas DataFrame or an HTML table.
    """

    def __init__(self, collection: str):
        """
        Initialize the Database with the specified collection.

        :param collection: String name of the MongoDB collection to manage.
        """
        # Loads the environment variables from .env file
        load_dotenv()

        """
        Initializes the MongoDB client with the URL from environment variables
        and sets the SSL certificate file location.
        It selects a database named 'Database'
        """
        self.database = MongoClient(getenv("MONGO_URL"), tlsCAFile=where())['Database']

        # Set the collection
        self.collection = self.database[collection]

    def seed(self, amount=2000) -> bool:
        """
        Seed the database with a given amount of Monster data.

        :param amount: The number of Monster data entries to create.
        :return: Boolean indicating if the operation was acknowledged.
        """

        data = [Monster().to_dict() for _ in range(amount)]
        return self.collection.insert_many(data).acknowledged

    def reset(self) -> dict:
        """
        Reset the database by deleting all documents within the collection.

        :return: The result of the delete operation.
        """
        return self.collection.delete_many({})

    def count(self) -> int:
        """
        Count the number of documents in the collection.

        :return: The number of documents.
        """
        return self.collection.count_documents({})

    def dataframe(self, query: Optional[Dict] = None) -> DataFrame:
        """
        Convert the documents in the collection to a pandas DataFrame.

        :param query: Optional query to filter the documents.
        :return: DataFrame with the collection's data.
        """

        # If no query is specified, the default is to fetch all documents
        return DataFrame(list(self.collection.find(query or {}, {'_id': False})))

    def html_table(self) -> str:
        """
        Convert the collection's data to an HTML table.

        :return: String containing an HTML table, or None if empty.
        """
        return self.dataframe().to_html()    

    if __name__ == '__main__':
        APP.run(debug=True)




    
    # class TestDatabase(unittest.TestCase):
    # def setUp(self):
    #     # Create a Database instance
    #     self.db = Database('test_collection')

    # def tearDown(self):
    #     # Reset the database after each test
    #     self.db.reset()

    # def test_reset(self):
    #     # Seed the database with some data
    #     self.db.seed(amount=10)

    #     # Check if there are documents in the collection before reset
    #     count_before_reset = self.db.count()
    #     self.assertTrue(count_before_reset > 0)

    #     # Reset the database
    #     self.db.reset()

        # Check if the collection is empty after reset
        # count_after_reset = self.db.count()
        # self.assertEqual(count_after_reset, 0)


# if __name__ == "__main__":
    # Run the tests if this file is executed directly
    # unittest.main()


# if __name__ == "__main__":
#     # This section is for testing the functionality of the Database class.
#     load_dotenv()
#     db_instance = Database('Database')
#     db_instance.reset()
#     db_instance.seed(1500)
#     print(db_instance.count())
#     print(db_instance.dataframe())
#     print(db_instance.html_table())
