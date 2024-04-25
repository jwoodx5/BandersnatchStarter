from data import Database  # Assuming your main code is in 'data.py' and your class is 'Database'

# Create an instance of the Database class
db = Database('your_collection_name')  # Replace 'your_collection_name' with the actual name of your MongoDB collection
db.reset()  # Clears existing data
db.seed()  # Seeds the database
print(f"Entries after seeding: {db.count()}")  # Should print 2000 if everything is correct