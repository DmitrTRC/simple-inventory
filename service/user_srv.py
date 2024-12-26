import sqlite3

from email_validator import EmailNotValidError

from mini_orm import ORM
from models.models import User
from utils.utils import is_email_valid


def add_user(orm: ORM, user: User):
    try:
        correct_email = is_email_valid(user.email)
        user.email = correct_email
        user_data = vars(user)  # converts user object to dict
        orm.insert_item('users', user_data)
    except EmailNotValidError as e:
        print(e)

def get_all_users(orm: ORM, table_name: str):
    query = f'SELECT * FROM {table_name};'
    try:
        cursor = orm.get_cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            print(f'User: {row}')
    except sqlite3.Error as e:
        print(f'An error occurred: {e}')