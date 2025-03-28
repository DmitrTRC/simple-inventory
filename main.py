import asyncio
import logging

from lazy_orm.db_manager import DatabaseManager
from model.todo_model import Todo, Category
from service.todo_srv import add_todo, get_all_todos
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


TODOS_DB_NAME = 'todos'
SAMPLE_TODOS = [
    Todo(task="Buy groceries", category=Category.SHOPPING),
    Todo(task="Read 'Clean Code'", category=Category.READING),
    Todo(task="Watch Python tutorial", category=Category.WATCHING),
    Todo(task="Schedule car maintenance", category=Category.MAINTENANCE),
    Todo(task="Plan birthday party", category=Category.BIRTHDAY)
]


async def _add_sample_todos(db_manager):
    """Add sample tasks to the database."""
    for task in SAMPLE_TODOS:
        result = add_todo(db_manager, task)
        logging.info(result) if result else logging.error('Error adding new Task!')


async def main():
    db_manager = DatabaseManager(USERS_DB_NAME)
    await _add_sample_users(db_manager)
    users = await get_all_users(db_manager)
    for user in users:
        print(user)

    todo_manager = DatabaseManager(TODOS_DB_NAME)
    await _add_sample_todos(todo_manager)
    tasks = await get_all_todos(todo_manager)
    for task in tasks:
        print(task)


if __name__ == '__main__':
    setup_logging()
    asyncio.run(main())
