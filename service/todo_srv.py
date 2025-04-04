from typing import List, Optional
from lazy_orm.db_manager import DatabaseManager, DatabaseError
import logging

from model.todo_model import Todo

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
    Logs the addition of a new Task.
    """
    logger.info(f'New Task {task} in category: {category} added.')


def _add_todo(
        db_manager: DatabaseManager, column_values: dict, log_message: str
) -> Optional[str]:
    """
    Helper function to add a task to the database and log the action.
    """
    try:
        db_manager.insert_row(TODOS_TABLE, column_values)
        logger.info(log_message)
        return 'Todo added successfully.'
    except DatabaseError as e:
        logger.exception(f"Error adding todo: {e}")
        return None


def add_todo(db_manager: DatabaseManager, todo: Todo) -> Optional[str]:
    """
    Adds a new task to the database if they do not already exist.
    """

    if is_todo_exists(db_manager, todo.task, todo.category.name):
        return 'User already exists!'

    column_values = {
        'task': todo.task,
        'category': todo.category.name,
        'date_added': todo.date_added,
        'date_completed': todo.date_completed,
        'status': todo.status.value
    }
    return _add_todo(db_manager, column_values, f'New Todo {todo.task} added.')


async def add_welcome_todo(db_manager: DatabaseManager) -> None:
    """
    Adds a welcome Task to the database.
    """
    column_values = {
        'task': 'Welcome to your Todo Manager!',
    }
    _add_todo(db_manager, column_values, 'Welcome task added successfully.')


async def handle_empty_todos(db_manager: DatabaseManager) -> None:
    """
    Adds a Welcome task if the database has no tasks.
    """
    await add_welcome_todo(db_manager)
    logger.info('No tasks found. Welcome task has been added.')


async def get_all_todos(db_manager: DatabaseManager) -> List[dict]:
    """
    Fetches all todos from the database or adds a Welcome task  if there are no tasks.
    """
    try:
        todos = await db_manager.fetch_all_rows(TODOS_TABLE, TODO_COLUMNS)

        if not todos:
            await handle_empty_todos(db_manager)
            todos = await db_manager.fetch_all_rows(TODOS_TABLE, TODO_COLUMNS)
        return todos

    except DatabaseError as e:
        logger.exception(f"Error fetching tasks: {e}")
        return []
