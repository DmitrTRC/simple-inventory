from typing import List, Optional
from lazy_orm.db_manager import DatabaseManager, DatabaseError
import logging

from model.todo_model import Todo, Status

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


async def _add_todo(
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


async def add_todo(db_manager: DatabaseManager, todo: Todo) -> Optional[str]:
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
    return  await _add_todo(db_manager, column_values, f'New Todo {todo.task} added.')


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


async def delete_todo_by_id(db_manager: DatabaseManager, task_id: int) -> bool:
    """
    Deletes a task from the database by its ID.
    """

    try:
        db_manager.delete_row(TODOS_TABLE, task_id)
        logger.info(f'Task with ID {task_id} deleted successfully.')
        return True
    except DatabaseError as e:
        logger.exception(f"Error deleting task with ID {task_id}: {e}")
        return False


async def update_todo_by_id(db_manger: DatabaseManager, task_id: int, new_task: str) -> bool:
    try:
        condition = f"id = {task_id}"
        column_values = {"task": new_task}
        db_manger.update_rows("todos", column_values, condition)
        return True
    except DatabaseError as e:
        logger.exception(f"Error updating task with ID {task_id}: {e}")
        return False


async def get_id_by_order_number(db_manager: DatabaseManager, order_number: int) -> int:
    """
    Get id by list order number  
    """
    try:
        todos = await db_manager.fetch_all_rows(TODOS_TABLE, ['id'])
        if 0 < order_number <= len(todos):
            return todos[order_number - 1]['id']
        else:
            raise IndexError("Order number out of range.")
    except (DatabaseError, IndexError) as e:
        logger.exception(f"Error fetching ID for order number {order_number}: {e}")
        raise e


async def set_status(db_manager: DatabaseManager, task_id: int, status: Status) -> bool:
    """
    Updates the status of a task in the database by its ID.
    """
    try:
        condition = f"id = {task_id}"
        column_values = {"status": status.value}
        db_manager.update_rows(TODOS_TABLE, column_values, condition)
        logger.info(f"Task with ID {task_id} status updated to {status.name}.")
        return True
    except DatabaseError as e:
        logger.exception(f"Error updating status for task with ID {task_id}: {e}")
        return False
