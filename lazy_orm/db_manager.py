import os
import sqlite3
from typing import Any, Dict, List, Optional

import logging

logging.getLogger().setLevel(logging.INFO)


class DatabaseError(Exception):
    """
    Custom exception class for database-related errors.

    This exception is raised when there is an issue related to database operations or interactions.

    :param message: A descriptive error message providing details about the database error.
    :type message: str
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DatabaseManager:
    """
    A class to manage SQLite database operations, including creating, reading, updating, and deleting records, as well as initializing and checking database existence.
    """

    def __init__(self, db_name: str, db_dir: str = 'data') -> None:
        """
        Initializes the DatabaseManager with specified database name and directory.

        Args:
            db_name (str): The name of the SQLite database file.
            db_dir (str): The directory where the database file is located.
        """
        self.db_path: str = os.path.join(db_dir, db_name)
        self.conn: sqlite3.Connection = self._connect_to_db()
        self.__cursor: sqlite3.Cursor = self.conn.cursor()
        self.__db_name = db_name
        self._check_db_exists()

    def __del__(self) -> None:
        """Destructor to close the SQLite connection."""
        if self.conn:
            self.conn.close()
            logging.info('Connection closed successfully.')

    def _connect_to_db(self) -> sqlite3.Connection:
        """
        Connects to the SQLite database, creating the directory if it does not exist.

        Returns:
            sqlite3.Connection: The SQLite connection object.
        """
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.OperationalError as e:
            logging.exception(f'Operational Error {e} when trying ti connect ro {self.db_path}')
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            return sqlite3.connect(self.db_path)
        except Exception as e:
            raise DatabaseError(f"Failed to connect to the database: {e}")

    @staticmethod
    def _row_to_dict(row: tuple, columns: List[str]) -> Dict[str, Any]:
        """
        Converts a row tuple to a dictionary mapping column names to their values.

        Args:
            row (tuple): A tuple representing a row of data.
            columns (List[str]): A list of column names corresponding to the tuple values.

        Returns:
            Dict[str, Any]: A dictionary where keys are column names and values are the corresponding row values.
        """
        return {column: row[idx] for idx, column in enumerate(columns)}

    def insert(self, table: str, column_values: Dict[str, Any]) -> None:
        """
        Inserts a row into the specified table.

        Args:
            table (str): The table name.
            column_values (Dict[str, Any]): A dictionary of column names and values to insert.
        """
        columns = ', '.join(column_values.keys())
        values = tuple(column_values.values())
        placeholders = ", ".join("?" * len(column_values))

        try:
            query = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
            self.__cursor.execute(query, values)
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Insert operation failed: {e.args[0]}")

    async def fetch_all(self, table: str, columns: List[str]) -> List[Dict[str, Any]]:
        """
        Fetches all rows from the specified table.

        Args:
            table (str): The table name.
            columns (List[str]): A list of column names to fetch.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the fetched rows.
        """
        columns_str = ", ".join(columns)
        try:
            query = f'SELECT {columns_str} FROM {table}'
            self.__cursor.execute(query)
            rows = self.__cursor.fetchall()
            return [self._row_to_dict(row, columns) for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Fetch operation failed: {e.args[0]}")

    def fetch_if(self, table: str, condition: str, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Fetches all rows from the specified table, where condition is True with given columns.

        Args:
            table (str): The table name.
            condition (str): The condition for fetching rows.
            columns (List[str], optional): A list of column names to fetch. Defaults to '*'.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the fetched rows.
        """
        columns_str = '*' if columns is None else ', '.join(columns)
        try:
            query = f"SELECT {columns_str} FROM {table} WHERE {condition}"
            self.__cursor.execute(query)
            rows = self.__cursor.fetchall()
            col_names = [desc[0] for desc in self.__cursor.description]
            return [self._row_to_dict(row, col_names) for row in rows]
        except sqlite3.Error as e:
            raise DatabaseError(f"Fetch operation with condition failed: {e.args[0]}")

    def delete(self, table: str, row_id: int) -> None:
        """
        Deletes a row from the specified table by its ID.

        Args:
            table (str): The table name.
            row_id (int): The ID of the row to delete.
        """
        try:
            query = f'DELETE FROM {table} WHERE id = ?'
            self.__cursor.execute(query, (row_id,))
            self.conn.commit()
            logging.info(f'Deletion of the user with ID = {row_id} is complete')
        except sqlite3.Error as e:
            raise DatabaseError(f"Delete operation failed: {e.args[0]}")

    def get_cursor(self) -> sqlite3.Cursor:
        """
        Returns the cursor object.

        Returns:
            sqlite3.Cursor: The cursor object.
        """
        return self.__cursor

    def update(self, table: str, column_values: Dict[str, Any], condition: str) -> None:
        """
        Updates rows in the specified table based on the given condition.

        Args:
            table (str): The table name.
            column_values (Dict[str, Any]): A dictionary of column names and values to update.
            condition (str): The condition for updating rows.
        """
        columns = ', '.join(f"{col} = ?" for col in column_values.keys())
        values = list(column_values.values())
        query = f"UPDATE {table} SET {columns} WHERE {condition}"

        try:
            self.__cursor.execute(query, values)
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"Update operation failed: {e.args[0]}")

    def get_table_size(self, table: str) -> int:
        """
        Returns the number of rows in the table.

        Args:
            table (str): The table name.

        Returns:
            int: The total number of rows.
        """
        try:
            query = f'SELECT COUNT(*) FROM {table}'
            self.__cursor.execute(query)
            return self.__cursor.fetchone()[0]
        except sqlite3.Error as e:
            raise DatabaseError(f"Get table size operation failed: {e.args[0]}")

    def _init_db(self, start_path=None) -> None:
        """
        Initializes the database by executing SQL commands from 'create_users_db.sql' file.
        """
        try:
            logging.info(f'Current Path: {os.getcwd()}')

            if start_path is None:
                start_path = 'sql'

            generic_creator_file = os.path.join(start_path, f'create_{self.__db_name}_db.sql')

            with open(os.path.join(generic_creator_file)) as fd:
                sql = fd.read()

            self.__cursor.executescript(sql)
            self.conn.commit()

            logging.info(f'Database {self.__db_name} initialized successfully!')
        except (FileNotFoundError, sqlite3.Error) as e:
            raise DatabaseError(f'Database initialization failed: {e}')

    def _check_db_exists(self) -> None:
        """
        Checks if the required tables exist in the database, and initializes the database if not.
        """
        try:

            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.__db_name}'"
            self.__cursor.execute(query)

            table_exists = self.__cursor.fetchall()
            if not table_exists:
                logging.warning('Table does not exist! ')
                self._init_db()
            else:
                logging.info(f'Database {self.db_path} exists and checked!')
        except sqlite3.Error as e:
            raise DatabaseError(f"Check database existence operation failed: {e.args[0]}")
