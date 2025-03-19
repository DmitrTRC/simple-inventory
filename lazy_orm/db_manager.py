import os
import sqlite3
from typing import Any, Dict, List, Optional
import logging


# Constants for default paths and file names
DEFAULT_DB_DIR = 'data'
DEFAULT_SQL_DIR = 'sql'
CREATE_DB_SCRIPT_TEMPLATE = 'create_{db_name}_db.sql'
SQLITE_MASTER_TABLE = 'sqlite_master'
TABLE_TYPE = 'table'

# General Placeholder Constants
WILDCARD_COLUMNS = '*'


class DatabaseError(Exception):
    """
    Custom exception class for database-related errors.

    This exception is raised when there is an issue related to database operations or interactions.

    Attributes:
        message (str): A descriptive error message providing details about the database error.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DatabaseManager:
    """
    A class to manage SQLite database operations.

    Handles database creation, reading, updating, and deletion operations. It also verifies the existence of required
    tables and initializes them if necessary.
    """

    def __init__(self, db_name: str, db_dir: str = DEFAULT_DB_DIR) -> None:
        """
        Initializes the DatabaseManager with specified database name and directory.

        Args:
            db_name (str): The name of the SQLite database file.
            db_dir (str): The directory where the database file is located.
        """
        self.db_name = db_name
        self.db_path: str = os.path.join(db_dir, db_name)  # Full path to the database file
        self.conn: sqlite3.Connection = self._connect_to_db()  # Initialize database connection
        self.cursor: sqlite3.Cursor = self.conn.cursor()  # Initialize the database cursor
        self._check_db_exists()  # Verify if the database exists

    def __del__(self) -> None:
        """Destructor to close the SQLite connection."""
        if self.conn:
            logging.info('Closing database connection.')
            self.conn.close()

    def _connect_to_db(self) -> sqlite3.Connection:
        """
        Connects to the SQLite database, creating the directory if it does not exist.

        Returns:
            sqlite3.Connection: The SQLite connection object.
        """
        try:
            logging.info(f"Connecting to database at {self.db_path}...")
            return sqlite3.connect(self.db_path)
        except sqlite3.OperationalError as e:
            logging.exception(f"SQLite Operational Error: {e}. Attempting to create directory for the database.")
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            return sqlite3.connect(self.db_path)
        except Exception as e:
            logging.exception("Unexpected error occurred while connecting to the database.")
            raise DatabaseError(f"Failed to connect to the database: {str(e)}")

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
            logging.info(f"Executing query: {query} with values: {values}")
            self.cursor.execute(query, values)
            self.conn.commit()
            logging.info(f"Successfully inserted into table '{table}'.")
        except sqlite3.Error as e:
            logging.exception("Insert operation failed.")
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
            logging.info(f"Executing query: {query}")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            logging.info(f"Successfully fetched {len(rows)} rows from table '{table}'.")
            return [self._row_to_dict(row, columns) for row in rows]
        except sqlite3.Error as e:
            logging.exception("Fetch operation failed.")
            raise DatabaseError(f"Fetch operation failed: {e.args[0]}")

    def fetch_if(self, table: str, condition: str, columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Fetches rows from the specified table based on a condition.

        Args:
            table (str): The table name.
            condition (str): The condition for fetching rows (e.g., "id > 10").
            columns (List[str], optional): A list of column names to fetch. Defaults to '*'.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the fetched rows.
        """
        columns_str = WILDCARD_COLUMNS if columns is None else ', '.join(columns)
        try:
            query = f"SELECT {columns_str} FROM {table} WHERE {condition}"
            logging.info(f"Executing query: {query}")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            col_names = [desc[0] for desc in self.cursor.description]
            logging.info(f"Successfully fetched {len(rows)} rows from table '{table}' with condition '{condition}'.")
            return [self._row_to_dict(row, col_names) for row in rows]
        except sqlite3.Error as e:
            logging.exception("Fetch with condition operation failed.")
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
            logging.info(f"Executing query: {query} with ID = {row_id}")
            self.cursor.execute(query, (row_id,))
            self.conn.commit()
            logging.info(f"Successfully deleted row with ID = {row_id} from table '{table}'.")
        except sqlite3.Error as e:
            logging.exception("Delete operation failed.")
            raise DatabaseError(f"Delete operation failed: {e.args[0]}")

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
            logging.info(f"Executing query: {query} with values: {values}")
            self.cursor.execute(query, values)
            self.conn.commit()
            logging.info(f"Successfully updated rows in table '{table}' with condition '{condition}'.")
        except sqlite3.Error as e:
            logging.exception("Update operation failed.")
            raise DatabaseError(f"Update operation failed: {e.args[0]}")

    def get_table_size(self, table: str) -> int:
        """
        Returns the number of rows in the table.

        Args:
            table (str): The table name.

        Returns:
            int: The total number of rows in the table.
        """
        try:
            query = f'SELECT COUNT(*) FROM {table}'
            logging.info(f"Executing query: {query}")
            self.cursor.execute(query)
            count = self.cursor.fetchone()[0]
            logging.info(f"Table '{table}' contains {count} rows.")
            return count
        except sqlite3.Error as e:
            logging.exception("Get table size operation failed.")
            raise DatabaseError(f"Get table size operation failed: {e.args[0]}")

    def _init_db(self, start_path: Optional[str] = None) -> None:
        """
        Initializes the database by executing SQL commands from the schema file.
        """
        try:
            logging.info("Initializing database...")
            start_path = start_path or DEFAULT_SQL_DIR
            schema_file = os.path.join(start_path, CREATE_DB_SCRIPT_TEMPLATE.format(db_name=self.db_name))
            logging.info(f"Reading schema file: {schema_file}")
            with open(schema_file) as fd:
                sql = fd.read()
            self.cursor.executescript(sql)
            self.conn.commit()
            logging.info(f"Database '{self.db_name}' initialized successfully!")
        except (FileNotFoundError, sqlite3.Error) as e:
            logging.exception("Database initialization failed.")
            raise DatabaseError(f"Database initialization failed: {e}")

    def _check_db_exists(self) -> None:
        """
        Checks if the required database tables exist, and initializes the database if they do not.
        """
        try:
            query = f"SELECT name FROM {SQLITE_MASTER_TABLE} WHERE type='{TABLE_TYPE}' AND name='{self.db_name}'"
            logging.info(f"Executing query: {query}")
            self.cursor.execute(query)
            table_exists = self.cursor.fetchone()
            if not table_exists:
                logging.warning(f"Table '{self.db_name}' does not exist. Initializing database...")
                self._init_db()
            else:
                logging.info(f"Database '{self.db_name}' exists and is ready.")
        except sqlite3.Error as e:
            logging.exception("Check database existence operation failed.")
            raise DatabaseError(f"Check database existence operation failed: {e.args[0]}")

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
