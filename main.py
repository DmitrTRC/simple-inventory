import sys

from lazy_orm.db_manager import DatabaseManager
from model.user_model import User
from service.user_srv import get_all_users, add_user

import logging

USERS_DB_NAME = 'users.db'


def main():
    db_manager = DatabaseManager(USERS_DB_NAME)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
