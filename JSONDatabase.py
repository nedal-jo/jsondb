import json
import os
from tabulate import tabulate

class JSONDatabase:
    def __init__(self, db_dir):
        # Ensure the database directory exists, and create it if it doesn't.
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
        self.db_dir = db_dir
    def create_collection(self, collection_name):
        collection_path = os.path.join(self.db_dir, f"{collection_name}.json")
        if not os.path.exists(collection_path):
            with open(collection_path, 'w') as file:
                json.dump([], file)
        else:
            print(f"Collection '{collection_name}' already exists.")

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

    def html_export(self, collection_name, html_file, custom_headers=None, query=None):
        collection_data = self.get_collection(collection_name)
        if query:
            collection_data = self.filter_data(collection_name, query)

        if not collection_data:
            print("No data found.")
            return

        if custom_headers:
            headers = custom_headers
        else:
            headers = collection_data[0].keys()
        
        data = [item.values() for item in collection_data]

        # Generate HTML table
        html_table = tabulate(data, headers, tablefmt="html")

        # Save HTML table to the specified file
        html_file_path = os.path.join(self.db_dir, f"{html_file}.html")
        with open(html_file_path, 'w') as html_file:
            html_file.write(html_table)
        print(f"HTML table saved to '{html_file_path}'")
