from data import Database  

# Create an instance of the Database class
db = Database('Database')  
db.reset()  # Clears existing data
db.seed()  # Seeds the database
print(f"Entries after seeding: {db.count()}")  

