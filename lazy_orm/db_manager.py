import os
import sqlite3
from typing import Any, Dict, List, Optional, TypeAlias
import logging

# A custom type alias for better readability of return types
RowList: TypeAlias = List[Dict[str, Any]]


class DatabaseError(Exception):
    """Custom exception for database-related errors."""

    def __init__(self, message: str) -> None:
        """
        Args:
             message (str): The error message to be passed to the Exception class constructor.
        """
        super().__init__(message)


class DatabaseManager:
    """
    A manager class to handle SQLite database operations.

    This class provides methods to create a database connection, perform basic
    CRUD operations (create, read, update, delete), and manage tables
    efficiently. It includes error handling, logging, and an initialization
    mechanism to prepare new databases if needed.
    """

    DEFAULT_DATABASE_DIRECTORY = 'data'
    SQL_WILDCARD_ALL_COLUMNS = '*'

    def __init__(self, db_name: str, db_dir: str = DEFAULT_DATABASE_DIRECTORY) -> None:
        """
        Initializes the DatabaseManager instance.

        Args:
            db_name (str): The name of the SQLite database file.
            db_dir (str): The directory path where the database file is stored.
        """
        self.database_path = os.path.join(db_dir, db_name)
        self.connection = self._initialize_database_connection()
        self.cursor = self.connection.cursor()
        self._ensure_database_existence()

    def __del__(self) -> None:
        """
        Destructor to cleanly close the SQLite connection when the instance is destroyed.
        """
        if self.connection:
            logging.info('Closing the database connection.')
            self.connection.close()

    def _initialize_database_connection(self) -> sqlite3.Connection:
        """
        Establishes the SQLite database connection.

        If the database directory does not exist, it will create it.

        Returns:
            sqlite3.Connection: The connection object for the database.

        Raises:
            DatabaseError: If the connection fails due to unexpected errors.
        """
        try:
            logging.info(f"Connecting to the database at {self.database_path}...")
            return sqlite3.connect(self.database_path)
        except sqlite3.OperationalError as operational_error:
            logging.exception(f"SQLite Operational Error: {operational_error}. Creating the database directory.")
            os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
            return sqlite3.connect(self.database_path)
        except Exception as exception:
            logging.exception("Unexpected error occurred during database connection.")
            raise DatabaseError(f"Failed to connect to the database: {exception}")

    def insert_row(self, table_name: str, column_values: Dict[str, Any]) -> None:
        """
        Inserts a row into the specified table.

        Args:
            table_name (str): The name of the database table.
            column_values (Dict[str, Any]): A dictionary mapping column names to values.

        Raises:
            DatabaseError: If the insert operation fails.
        """
        columns = ', '.join(column_values.keys())
        placeholders = ', '.join(['?'] * len(column_values))
        values = list(column_values.values())
        query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
        self._execute_query(query, values, operation_context=f"Insertion into table '{table_name}' failed.")

    async def fetch_all_rows(self, table_name: str, column_names: List[str]) -> RowList:
        """
        Fetches all rows from the specified table.

        Args:
            table_name (str): The name of the table to fetch rows from.
            column_names (List[str]): The list of column names to retrieve.

        Returns:
            RowList: A list of dictionaries representing each row of the result.

        Raises:
            DatabaseError: If the fetch operation fails.
        """
        columns_str = ', '.join(column_names)
        query = f"SELECT {columns_str} FROM {table_name}"
        return self._execute_query(query, fetch_mode=True, operation_context="Fetch all rows")

    def fetch_rows_if(
            self, table_name: str, condition: str, column_names: Optional[List[str]] = None
    ) -> RowList:
        """
        Fetches rows from the specified table that match a given condition.

        Args:
            table_name (str): The name of the table to query.
            condition (str): The WHERE clause condition for the query.
            column_names (Optional[List[str]]): A list of specific columns to retrieve. Defaults to all columns.

        Returns:
            RowList: A list of dictionaries for each matching row.

        Raises:
            DatabaseError: If the operation fails.
        """
        columns_str = self.SQL_WILDCARD_ALL_COLUMNS if column_names is None else ', '.join(column_names)
        query = f"SELECT {columns_str} FROM {table_name} WHERE {condition}"
        return self._execute_query(query, fetch_mode=True, operation_context=f"Fetch rows with condition '{condition}'")

    def delete_row(self, table_name: str, row_id: int) -> None:
        """
        Deletes a row from the specified table by its ID.

        Args:
            table_name (str): The name of the table.
            row_id (int): The ID of the row to delete.

        Raises:
            DatabaseError: If the delete operation fails.
        """
        query = f"DELETE FROM {table_name} WHERE id = ?"
        self._execute_query(query, [row_id], operation_context=f"Deletion of row with ID '{row_id}' failed.")

    def update_rows(self, table_name: str, column_values: Dict[str, Any], condition: str) -> None:
        """
        Updates rows in the specified table that match a condition.

        Args:
            table_name (str): The name of the table to update.
            column_values (Dict[str, Any]): A dictionary mapping columns to their new values.
            condition (str): The WHERE clause condition for the update.

        Raises:
            DatabaseError: If the update operation fails.
        """
        set_clause = ', '.join([f"{col} = ?" for col in column_values.keys()])
        values = list(column_values.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self._execute_query(query, values, operation_context=f"Updating rows in table '{table_name}' failed.")

    def get_row_count(self, table_name: str) -> int:
        """
        Retrieves the total number of rows in the specified table.

        Args:
            table_name (str): The name of the table.

        Returns:
            int: The count of rows in the table.

        Raises:
            DatabaseError: If the row count query fails.
        """
        query = f"SELECT COUNT(*) AS row_count FROM {table_name}"
        result = self._execute_query(query, fetch_mode=True, operation_context=f"Counting rows in table '{table_name}'")
        return result[0]['row_count'] if result else 0

    def _ensure_database_existence(self) -> None:
        """
        Checks if the database exists and initializes it if necessary.
        """
        if not os.path.exists(self.database_path):
            logging.info(f"Database '{self.database_path}' not found. Initializing a new database.")
            self._initialize_database()

    def _initialize_database(self) -> None:
        """
        Performs initial database setup using an SQL script if available.
        """
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
        """
        try:
            init_script_path = os.path.join(self.DEFAULT_DATABASE_DIRECTORY, 'init.sql')
            if os.path.exists(init_script_path):
                logging.info(f"Running initialization script: {init_script_path}")
                with open(init_script_path, 'r') as script_file:
                    sql_script = script_file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()
                logging.info("Database initialized successfully.")
            else:
                logging.warning("No initialization script found. Skipping setup.")
        except sqlite3.Error as error:
            logging.exception("Database initialization failed.")
            raise DatabaseError(f"Failed to initialize database: {error}")

    def _execute_query(
            self,
            query: str,
            params: Optional[List[Any]] = None,
            fetch_mode: bool = False,
            operation_context: str = "SQL Operation"
    ) -> Optional[RowList]:
        """
        Executes a given SQL query with optional parameter binding and result fetching.

        Args:
            query (str): The SQL query to execute.
            params (Optional[List[Any]]): Parameters for the query placeholders.
            fetch_mode (bool): If True, fetches and returns results.
            operation_context (str): A description of the specific operation for logging.

        Returns:
            Optional[RowList]: Fetched rows as a list of dictionaries if fetch_mode is True; otherwise None.

        Raises:
            DatabaseError: If the query execution fails.
        """
        try:
            logging.info(f"Executing query: {query}")
            self.cursor.execute(query, params or [])
            if fetch_mode:
                rows = self.cursor.fetchall()
                column_names = [description[0] for description in self.cursor.description]
                return [dict(zip(column_names, row)) for row in rows]
            self.connection.commit()
        except sqlite3.Error as error:
            logging.exception(f"{operation_context} failed.")
            raise DatabaseError(f"{operation_context}: {error}")
        return None
