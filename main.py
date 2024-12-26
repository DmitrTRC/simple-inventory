import asyncio
import sys
import time

from lazy_orm.db_manager import DatabaseManager
from model.user_model import User
from service.user_srv import get_all_users, add_user

import logging

USERS_DB_NAME = 'users'


async def main():
    db_manager = DatabaseManager(USERS_DB_NAME)

    users = await get_all_users(db_manager)
    add_user(db_manager, 'Arina', 'Arisha@librem.com', 20)

    for user in users:
        print(user)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
