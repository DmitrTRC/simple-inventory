import typer
from service.cli_todo_logic import run_async_task, create_task_main, list_tasks_main, \
    delete_task_main, update_task_main, set_done_main
from utils.logging_simp_inv import setup_logging

app = typer.Typer()


# Commands
@app.command('new', short_help='Create a new task')
def create_task(name: str, cat: str = 'BACKLOG'):
    """Create a new task."""
    run_async_task(create_task_main(name, cat))


@app.command('list', short_help='List all tasks')
def list_tasks():
    """List all tasks."""
    run_async_task(list_tasks_main())


@app.command('del', short_help='Delete a task by ID')
def delete_task(task_id: int):
    """Delete a task by its ID."""
    run_async_task(delete_task_main(task_id))


@app.command('update', short_help='Update a task by ID')
def update_task(task_id: int, new_name: str):
    """Update a task's name by ID."""
    run_async_task(update_task_main(task_id, new_name))


@app.command('done', short_help='Set task status to Done')
def set_done(task_id: int):
    """Set a task's status to done."""
    run_async_task(set_done_main(task_id))


# Entry point
if __name__ == '__main__':
    setup_logging()
    app()
