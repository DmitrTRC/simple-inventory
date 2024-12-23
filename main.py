import os
import sqlite3

from email_validator import validate_email, EmailNotValidError
from mini_orm import ORM
from models.models import User
from service.service import get_all_users, add_user




def main():
    db_name = 'users.db'
    orm = ORM(db_name)
    ORM.create_table(orm, 'users')

    add_user(orm, User(
        'Arina',
        'Arina@gmail.com',
        123456789,
        17
    ))

    add_user(orm, User(
        'Vlad',
        'Vlad@gmail.com',
        987654321,
        age=20
    ))

    get_all_users(orm, 'users')


if __name__ == '__main__':
    main()
