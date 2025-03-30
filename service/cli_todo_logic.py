from typing import List
from rich.console import Console
from rich.table import Table
from lazy_orm.db_manager import DatabaseManager
from model.todo_model import Category, Todo, Status
from service.todo_srv import add_todo, get_all_todos, get_id_by_index as get_id_by_index, logger, \
    delete_todo_by_id, update_todo_by_id, set_status

console = Console()

# Constants
DB_NAME = 'todos'
todo_manager = DatabaseManager(DB_NAME)

# Status symbols
COMPLETED_STATUS_SYMBOL = 'Completed'
UNDONE_STATUS_SYMBOL = '📌'


# Adding a utility to `Status` enum for cleaner symbol logic.
def get_status_symbol(self) -> str:
    return COMPLETED_STATUS_SYMBOL if self == Status.DONE else UNDONE_STATUS_SYMBOL


# Extracted a function to manage row creation for reuse and better readability
def create_task_row(todo_item: dict, index: int) -> List[str]:
    return [
        str(index),
        str(todo_item.get('task', "N/A")),
        str(todo_item.get('category', "N/A")),
        str(todo_item.get('date_added', "N/A")),
        str(todo_item.get('date_completed', "N/A")),
        get_status_symbol(Status(int(todo_item.get('status', 0))))
    ]


# Utility function to validate category
def validate_category(cat: str) -> Category:
    """
    :param cat: The category name as a string to be validated.
    :type cat: str
    :return: The matched Category enum member.
    :rtype: Category
    :raises ValueError: If the provided category is invalid or not found in Category enum members.
    """
    if not cat or cat.upper() not in Category.__members__:
        error_msg = f"'{cat}' is not a valid category. Valid options are: {', '.join(Category.__members__.keys())}"
        console.print(f"[red]Error: {error_msg}[/red]")
        raise ValueError(error_msg)
    return Category[cat.upper()]


# Renamed variables for clarity
def display_tasks(task_list: List[dict]):
    """
    Display tasks in a formatted table.
    :param task_list: A list of dictionaries representing task items.
    :return: None
    """
    if not task_list:
        console.print("[yellow]No tasks found![/yellow]")
        return

    table = Table(title="To-Do List")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Date Added", style="yellow")
    table.add_column("Date Completed", style="blue")
    table.add_column("Status", style="green", justify="center", min_width=10)

    for index, todo_item in enumerate(task_list, start=1):
        table.add_row(*create_task_row(todo_item, index))

    console.print(table)


async def create_task_main(name: str, cat: str):
    """
    :param name: The name of the task to be created
    :param cat: The category of the task to be validated and assigned
    :return: None
    """
    try:
        category = validate_category(cat)
        await add_todo(todo_manager, Todo(name, category=category))
        console.print(f"[green]Task '{name}' created successfully![/green]")
        await list_tasks_main()
    except ValueError:
        pass  # Validation error already handled with a console message
    except Exception as e:
        console.print(f"[red]Failed to create task: {e}[/red]")


async def list_tasks_main():
    """
    Asynchronously fetches all todos and displays them. Handles exceptions by printing an error message to the console.

    :return: None
    """
    try:
        todos = await get_all_todos(todo_manager)
        display_tasks(todos)
    except Exception as e:
        console.print(f"[red]Failed to fetch tasks: {e}[/red]")


async def delete_task_main(index: int):
    """
    Deletes a task by its ID and updates the task list. Logs the operation and provides feedback to the user on success or failure.

    :param index: The ID of the task to be deleted.
    :return: None
    """
    try:
        corresponded_id = await get_id_by_index(todo_manager, index)
        logger.debug(f"Corresponded id: {corresponded_id}")
        deleted = await delete_todo_by_id(todo_manager, corresponded_id)
        if deleted:
            console.print(f"[green]Task with ID {index} deleted successfully![/green]")
        else:
            console.print(f"[yellow]No task found with ID {index}.[/yellow]")
        await list_tasks_main()
    except Exception as e:
        console.print(f"[red]Failed to delete task: {e}[/red]")


async def update_task_main(index: int, new_name: str):
    """
    :param index: The unique integer identifier associated with the task to be updated.
    :param new_name: The new name or title for the specified task.
    :return: None. This function performs an update operation and prints messages to the console indicating the outcome.
    """
    if not new_name.strip():
        console.print("[red]Error: Task name cannot be empty.[/red]")
        return
    try:
        corresponded_id = await get_id_by_index(todo_manager, index)
        logger.debug(f"Corresponded id: {corresponded_id}")
        updated = await update_todo_by_id(todo_manager, corresponded_id, new_name)
        if updated:
            console.print(f"[green]Task with ID {index} updated successfully![/green]")
        else:
            console.print(f"[yellow]No task found with ID {index}.[/yellow]")
        await list_tasks_main()
    except Exception as e:
        console.print(f"[red]Failed to update task: {e}[/red]")


async def set_done_main(index: int):
    """
    Marks a task as done based on the given task ID.

    :param index: The ID of the task to be marked as done.
    :return: None
    """
    try:
        corresponded_id = await get_id_by_index(todo_manager, index)
        logger.debug(f"Corresponded id: {corresponded_id}")
        status = await set_status(todo_manager, corresponded_id, Status.DONE)
        if status:
            console.print(f"[green]Task with ID {index} marked as Done![/green]")
        else:
            console.print(f"[yellow]No task found with ID {index}.[/yellow]")
        await list_tasks_main()
    except Exception as e:
        console.print(f"[red]Failed to mark task as done: {e}[/red]")
