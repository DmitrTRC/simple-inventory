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
    """Create a new task."""
    execute_task(create_task_main, name, category)


@app.command('list', short_help='List all tasks')
def list_tasks():
    """List all tasks."""
    execute_task(list_tasks_main)


@app.command('delete', short_help='Delete a task by ID')
def delete_task(task_id: int):
    """Delete a task by its ID."""
    execute_task(delete_task_main, task_id)


@app.command('update', short_help='Update a task by ID')
def update_task(task_id: int, new_name: str):
    """Update a task's name by ID."""
    execute_task(update_task_main, task_id, new_name)


@app.command('done', short_help='Set task status to Done')
def set_done(task_id: int):
    """Set a task's status to done."""
    execute_task(set_done_main, task_id)


# Entry point
if __name__ == '__main__':
    setup_logging()
    app()
