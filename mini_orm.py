import sqlite3

class ORM:
    def __init__(self, db_name: str):
        #  TODO: Make connection and cursor Privates. Write getter for __cursor.
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def insert_item(self, table: str, data: dict):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        self.cursor.execute(query, values)
        self.connection.commit()

    def select_item(self):
        raise NotImplementedError

    def update_item(self):
        raise NotImplementedError

    def delete_item(self):
        raise NotImplementedError

    def fetch_one_item(self):
        raise NotImplementedError

    def fetch_all_items(self):
        raise NotImplementedError

# TODO: Write Destructor. Close connection! ( override __del__() , and if connnection : close connection )
