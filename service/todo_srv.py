from typing import List, Optional
from lazy_orm.db_manager import DatabaseManager, DatabaseError
import logging

# Setup logger
logger = logging.getLogger(__name__)

# Constants
TODOS_TABLE = 'todos'
TODO_COLUMNS = ['id', 'task', 'category', 'date_added', 'date_completed', 'status']


def is_todo_exists(db_manager: DatabaseManager, task: str, category: str) -> bool:
    """
    Checks if the task exists in the database based on task name.
    """
    condition = f'task="{task}" AND category="{category}"'
    todos = db_manager.fetch_rows_if(TODOS_TABLE, condition)
    return len(todos) > 0


def log_todo_addition(task: str, category: str) -> None:
    """
    Logs the addition of a new user.
    """
    logger.info(f'New Task {task} in category: {category} added.')


def _add_todo(
        db_manager: DatabaseManager, column_values: dict, log_message: str
) -> Optional[str]:
    """
    Helper function to add a user to the database and log the action.
    """
    try:
        db_manager.insert_row(TODOS_TABLE, column_values)
        logger.info(log_message)
        return 'Todo added successfully.'
    except DatabaseError as e:
        logger.exception(f"Error adding todo: {e}")
        return None


def add_todo(db_manager: DatabaseManager, task: str, category: str, age: int) -> Optional[str]:
    """
    Adds a new user to the database if they do not already exist.
    """
    normalized_email = validate_and_normalize_email(email)

    if is_user_exists(db_manager, username, normalized_email):
        return 'User already exists!'

    column_values = {
        'username': username,
        'email': normalized_email,
        'age': age,
    }
    return _add_user(db_manager, column_values, f'New User {username} added.')


async def add_admin_user(db_manager: DatabaseManager) -> None:
    """
    Adds a predefined admin user to the database.
    """
    column_values = {
        'username': 'Admin',
        'email': '9984398@gmail.com',
        'age': 100,
        'phone': '+79219984444',
    }
    _add_user(db_manager, column_values, 'Admin user added successfully.')


async def handle_empty_users(db_manager: DatabaseManager) -> None:
    """
    Adds an admin user if the database has no users.
    """
    await add_admin_user(db_manager)
    logger.info('No users found. Admin User has been added.')


async def get_all_users(db_manager: DatabaseManager) -> List[dict]:
    """
    Fetches all users from the database or adds an admin user if there are no users.
    """
    try:
        users = await db_manager.fetch_all_rows(USERS_TABLE, USER_COLUMNS)

        if not users:
            await handle_empty_users(db_manager)
            users = await db_manager.fetch_all_rows(USERS_TABLE, USER_COLUMNS)
        return users
    except DatabaseError as e:
        logger.exception(f"Error fetching users: {e}")
        return []
