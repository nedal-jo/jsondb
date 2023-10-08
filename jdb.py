import json
import os
from tabulate import tabulate

class JSONDatabase:
    def __init__(self, db_dir):
        self.db_dir = db_dir

    def create_collection(self, collection_name):
        collection_path = os.path.join(self.db_dir, f"{collection_name}.json")
        if not os.path.exists(collection_path):
            with open(collection_path, 'w') as file:
                json.dump([], file)

    def get_collection(self, collection_name):
        collection_path = os.path.join(self.db_dir, f"{collection_name}.json")
        if os.path.exists(collection_path):
            with open(collection_path, 'r') as file:
                return json.load(file)
        else:
            return []

    def insert_data(self, collection_name, data):
        collection_path = os.path.join(self.db_dir, f"{collection_name}.json")
        collection_data = self.get_collection(collection_name)
        collection_data.append(data)
        with open(collection_path, 'w') as file:
            json.dump(collection_data, file)

    def update_data(self, collection_name, query, new_data):
        collection_path = os.path.join(self.db_dir, f"{collection_name}.json")
        collection_data = self.get_collection(collection_name)
        updated_data = []
        for item in collection_data:
            if all(item.get(key) == value for key, value in query.items()):
                item.update(new_data)
            updated_data.append(item)
        with open(collection_path, 'w') as file:
            json.dump(updated_data, file)

    def delete_data(self, collection_name, query):
        collection_path = os.path.join(self.db_dir, f"{collection_name}.json")
        collection_data = self.get_collection(collection_name)
        updated_data = [item for item in collection_data if not all(item.get(key) == value for key, value in query.items())]
        with open(collection_path, 'w') as file:
            json.dump(updated_data, file)

    def filter_data(self, collection_name, query):
        collection_data = self.get_collection(collection_name)
        filtered_data = [item for item in collection_data if all(item.get(key) == value for key, value in query.items())]
        return filtered_data

    def print_tabulate(self, collection_name, query=None):
        collection_data = self.get_collection(collection_name)
        if query:
            collection_data = self.filter_data(collection_name, query)
        
        if not collection_data:
            print("No data found.")
            return
        
        headers = collection_data[0].keys()
        data = [item.values() for item in collection_data]
        print(tabulate(data, headers, tablefmt="grid"))

# Example usage:
if __name__ == "__main__":
    # Initialize the database with a directory to store JSON files.
    db = JSONDatabase('data')

    # Create a new collection/table.
    db.create_collection('users')

    # Insert 20 dummy records.
    for i in range(1, 21):
        user_data = {"id": i, "name": f"User {i}", "email": f"user{i}@example.com"}
        db.insert_data('users', user_data)

    # Print all users before any operations.
    print("All Users (Before Operations):")
    db.print_tabulate('users')

    # Update data in the 'users' collection.
    update_query = {"id": 1}
    new_data = {"email": "newemail@example.com"}
    db.update_data('users', update_query, new_data)
#
    print("\n(After update newemail Operations):")
    db.print_tabulate('users')


    # Delete data from the 'users' collection.
    delete_query = {"id": 2}
    db.delete_data('users', delete_query)

#
    print("\n(After delete id 2 Operations):")
    db.print_tabulate('users')

    # Filter data from the 'users' collection.
    filter_query = {"name": "User 3"}
    print("\nFiltered Users (After Operations):")
    db.print_tabulate('users', filter_query)
