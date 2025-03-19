import asyncio
import logging
from lazy_orm.db_manager import DatabaseManager
from service.user_srv import get_all_users, add_user
from utils.logging_simp_inv import setup_logging

USERS_DB_NAME = 'users'
SAMPLE_USERS = [
    {'username': 'Arina5', 'email': 'Arisha5@librem.com', 'age': 20},
    {'username': 'Alex', 'email': 'something@gmail.com', 'age': 40},
    {'username': 'Dmitry', 'email': 'morozovd@yandex.ru', 'age': 18}
]


async def _add_sample_users(db_manager):
    """Add sample users to the database."""
    for user in SAMPLE_USERS:
        result = add_user(db_manager, user['username'], user['email'], user['age'])
        logging.info(result) if result else logging.error('Error adding new User!')


async def main():
    db_manager = DatabaseManager(USERS_DB_NAME)
    await _add_sample_users(db_manager)
    users = await get_all_users(db_manager)
    for user in users:
        print(user)


if __name__ == '__main__':
    setup_logging()
    asyncio.run(main())
