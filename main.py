import asyncio
import sys
import time

from lazy_orm.db_manager import DatabaseManager
from model.user_model import User
from service.user_srv import get_all_users, add_user

from utils.logging import setup_logging

USERS_DB_NAME = 'users'


async def main():
    db_manager = DatabaseManager(USERS_DB_NAME)

    add_user(db_manager, 'Arina5', 'Arisha5@librem.com', 20)
    add_user(db_manager, 'Alex', 'something@gmail.com', 40)
    add_user(db_manager, 'Dmitry', 'morozovd@yandex.ru', 18)

    users = await get_all_users(db_manager)

    for user in users:
        print(user)


if __name__ == '__main__':
    setup_logging()
    asyncio.run(main())
