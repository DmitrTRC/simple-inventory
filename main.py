import os
import re
import sqlite3

from email_validator import validate_email, EmailNotValidError
from mini_orm import ORM

SQL_BASE_PATH = 'SQL/'


class User:
    def __init__(self, username, email, phone, age):
        self.username = username
        self.email = email
        self.phone = phone
        self.age = age


class TableOperations:
    @staticmethod
    def create_table(orm: ORM, table_name: str):
        sql_script_name = f'create_{table_name}.sql'
        script_path = os.path.join(SQL_BASE_PATH, sql_script_name)
        try:
            with open(script_path, 'r') as fd:
                sql_script = fd.read()
                orm.cursor.execute(sql_script)
                orm.connection.commit()
            print(f"Table '{table_name}' created successfully.")
        except FileNotFoundError:
            print(f"SQL script '{sql_script_name}' not found in path: {SQL_BASE_PATH}.")
        except sqlite3.Error as e:
            print(f"SQLite error during table creation: {e}")

    @staticmethod
    def add_user(orm: ORM, user: User):
        try:
            correct_email = TableOperations.is_email_valid(user.email)
            user.email = correct_email
            user_data = vars(user) # converts user object to dict
            orm.insert_item('users', user_data)
        except EmailNotValidError as e:
            print(e)

    @staticmethod
    def is_email_valid(email):
        try:
            v = validate_email(email)
            return v.normalized.lower()
        except EmailNotValidError as e:
            raise EmailNotValidError(f'Email format is not correct: {e}')

def get_all_users(orm: ORM, table_name: str):
    query = f'SELECT * FROM {table_name};'
    try:
        orm.cursor.execute(query)
        rows = orm.cursor.fetchall()
        for row in rows:
            print(f'User: {row}')
    except sqlite3.Error as e:
        print(f'An error occurred: {e}')


def main():
    db_name = 'users.db'
    orm = ORM(db_name)
    TableOperations.create_table(orm, 'users')

    TableOperations.add_user(orm, User(
        'Arina',
        'Arina@gmail.com',
        123456789,
        17
    ))

    TableOperations.add_user(orm, User(
        'Vlad',
        'Vlad@gmail.com',
        987654321,
        age=20
    ))

    get_all_users(orm, 'users')


if __name__ == '__main__':
    main()
