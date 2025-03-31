import asyncio
import typer

from service.cli_todo_logic import (
    create_task_main,
    list_tasks_main,
    delete_task_main,
    update_task_main,
    set_done_main, console
)
from utils.logging_simp_inv import setup_logging

DEFAULT_CATEGORY = 'BACKLOG'
app = typer.Typer()


# Async handler wrapper
def execute_task(coroutine, *args, **kwargs):
    """
    Executes the given coroutine either by creating a new task if the event loop is running or by running it directly in the event loop. Handles exceptions and logs errors.

    :param coroutine: The coroutine function to be executed.
    :param args: Positional arguments to pass to the coroutine.
    :param kwargs: Keyword arguments to pass to the coroutine.
    :return: None
    """
    loop = asyncio.get_event_loop()
    try:
        if loop.is_running():
            loop.create_task(coroutine(*args, **kwargs))
        else:
            asyncio.run(coroutine(*args, **kwargs))
    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")


# Commands
@app.command('new', short_help='Create a new task')
def create_task(name: str, category: str = DEFAULT_CATEGORY):
    """
    :param name: The name of the task to be created.
    :param category: The category of the task. Defaults to a predefined value if not provided.
    :return: None
    """
    execute_task(create_task_main, name, category)


@app.command('list', short_help='List all tasks')
def list_tasks():
    """
    List all tasks.

    This function is a command that serves as an interface to list all tasks. It invokes
    the main functionality by calling `list_tasks_main` through the `execute_task`
    function, which ensures the appropriate execution environment for the task.

    :return: None
    """
    execute_task(list_tasks_main)


@app.command('delete', short_help='Delete a task by ID')
def delete_task(task_id: int):
    """
    :param task_id: The ID of the task to be deleted.
    :return: None
    """
    execute_task(delete_task_main, task_id)


@app.command('update', short_help='Update a task by ID')
def update_task(task_id: int, new_name: str):
    """
    :param task_id: The identifier of the task to be updated.
    :param new_name: The new name to assign to the task.
    :return: None
    """
    execute_task(update_task_main, task_id, new_name)


@app.command('done', short_help='Set task status to Done')
def set_done(task_id: int):
    """
    :param task_id: The ID of the task to mark as done.
    :return: None
    """
    execute_task(set_done_main, task_id)


# Entry point
if __name__ == '__main__':
    setup_logging()
    app()
