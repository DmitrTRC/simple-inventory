from typing import List

from lazy_orm.db_manager import DatabaseManager, DatabaseError
from utils.email import validate_and_normalize_email

import logging

USERS_TABLE = 'users'
USERS_COLUMNS = ['id', 'email', 'username', 'phone', 'age']

def is_user_exists(db_manager: DatabaseManager, username: str, email: str) -> bool:
    """
    :param db_manager: The database manager instance used to interact with the database.
    :param username: The username of the user to check for existence in the database.
    :param email: The email of the user to check for duplication in the database.
    :return: A boolean value indicating whether the user exists (True) or not (False).
    """
    users = db_manager.fetch_if('users', f'username="{username}" OR email="{email}"')
    return len(users) > 0


def log_user_addition(username: str, email: str) -> None:
    """
    :param username: The username of the new user being added.
    :param email: The email address of the new user being added.
    :return: None
    """
    logging.info(f'New User {username} with email: {email} added.')


def add_user(orm: DatabaseManager, username: str, email: str, age: int) -> bool:
    """
    :param orm: Instance of the DatabaseManager used to interact with the database.
    :param username: The username of the user to be added to the database.
    :param email: The email address of the user to be added; it will be validated and normalized before insertion.
    :param age: The age of the user to be added to the database.
    :return: Returns True if the user is successfully added, otherwise returns False due to errors.
    """
    try:
        column_values = {
            'username': username,
            'email': validate_and_normalize_email(email),
            'age': age,
        }

        if is_user_exists(orm, username, email):
            raise DatabaseError('User is already exists!')

        orm.insert('users', column_values)
        log_user_addition(username, email)
        return True
    except DatabaseError as e:
        logging.exception(f"Error adding user: {e}")
        return False


async def add_admin_user(db_manager):
    """
    Adds an admin user to the database with predefined details.

    :param db_manager: The database manager instance responsible for handling database operations.
    :return: None
    """
    try:
        column_values = {
            'username': 'Admin',
            'email': '9984398@gmail.com',
            'age': 100,
            'phone': '+79219984444',
        }
        db_manager.insert('users', column_values)
        logging.info('Admin user added successfully.')
    except DatabaseError as e:
        logging.exception(f"Error adding admin user: {e}")


async def handle_empty_users(db_manager: DatabaseManager):
    """
    Handles the case when there are no users in the database by adding an admin user.

    :param db_manager: An instance of DatabaseManager used to interact with the database.
    :return: None
    """
    await add_admin_user(db_manager)
    logging.info('No users found. Admin User have been added.')


async def get_all_users(db_manager: DatabaseManager) -> List[dict]:
    try:
        users = await db_manager.fetch_all(USERS_TABLE, USERS_COLUMNS)
        if not users:
            await handle_empty_users(db_manager)
            users = await db_manager.fetch_all(USERS_TABLE, USERS_COLUMNS)
        return users
    except DatabaseError as e:
        logging.exception(f"Error fetching users: {e}")
        return []


