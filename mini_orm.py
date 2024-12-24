import os
import sqlite3

SQL_BASE_PATH = 'SQL/'


class ORM:
    def __init__(self, db_name: str):
        self.__connection = sqlite3.connect(db_name)
        self.__cursor = self.__connection.cursor()

    def get_cursor(self):
        return self.__cursor

    def get_connection(self):
        return self.__connection

    def create_table(self, table_name: str):
        sql_script_name = f'create_{table_name}.sql'
        script_path = os.path.join(SQL_BASE_PATH, sql_script_name)
        try:
            with open(script_path, 'r') as fd:
                sql_script = fd.read()
                self.__cursor.execute(sql_script)
                self.__connection.commit()
            print(f"Table '{table_name}' created successfully.")
        except FileNotFoundError:
            print(f"SQL script '{sql_script_name}' not found in path: {SQL_BASE_PATH}.")
        except sqlite3.Error as e:
            print(f"SQLite error during table creation: {e}")

    def insert_item(self, table: str, data: dict):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        values = tuple(data.values())
        query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        self.__cursor.execute(query, values)
        self.__connection.commit()

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

    def __del__(self):
        if self.__connection:
            self.__connection.close()
