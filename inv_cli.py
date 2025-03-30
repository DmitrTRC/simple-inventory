import typer
from rich.console import Console
from rich.table import Table

from lazy_orm.db_manager import DatabaseManager
from model.todo_model import Todo, Category, Status
from service.todo_srv import add_todo, get_all_todos, delete_todo_by_id, get_id_by_order_number, logger, \
    update_todo_by_id, set_status

from utils.logging_simp_inv import setup_logging

console = Console()

app = typer.Typer()

TODOS_DB_NAME = 'todos'
todo_manager = DatabaseManager(TODOS_DB_NAME)

import asyncio


@app.command('new', short_help='Create a new task')
def create_task(name: str, cat: str = 'BACKLOG'):
    # Use `asyncio.run` to call the asynchronous version of `create_task_main`
    asyncio.run(create_task_main(name, cat))


async def create_task_main(name: str, cat: str = 'BACKLOG'):
    if not cat or cat.upper() not in Category.__members__:
        console.print(
            f"[red]Error: '{cat}' is not a valid category. Valid options are: {', '.join(Category.__members__.keys())}[/red]"
        )
        return

    cat = Category[cat.upper()]
    try:
        add_todo(todo_manager, Todo(name, category=cat))
        console.print(f"Task '{name}' created successfully!")
        await list_tasks_main()  # Call the asynchronous function directly
    except Exception as e:
        console.print(f"[red]Failed to create task: {e}[/red]")


@app.command('list', short_help='List all tasks')
def list_tasks():
    # Use `asyncio.run` to call the asynchronous version of `list_tasks_main`
    asyncio.run(list_tasks_main())


async def list_tasks_main():
    todos = await get_all_todos(todo_manager)  # Await the asynchronous database call
    if not todos:
        console.print("[yellow]No tasks found![/yellow]")
        return

    table = Table(title="To-Do List")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Date Added", style="yellow")
    table.add_column("Date Completed", style="blue")
    table.add_column("Status", style="red", justify="center")

    for represent_number, todo_item in enumerate(todos, start=1):
        table.add_row(
            str(represent_number),
            str(todo_item.get('task', "N/A")),
            str(todo_item.get('category', "N/A")),
            str(todo_item.get('date_added', "N/A")),
            str(todo_item.get('date_completed', "N/A")),
            '✅' if todo_item.get('status') == '1' else '📌'
        )

    console.print(table)


@app.command('del', short_help='Delete a task by ID')
def delete_task(task_id: str):
    corresponded_id = asyncio.run(get_id_by_order_number(todo_manager, int(task_id)))
    logger.debug(f"Corresponded id: {corresponded_id}")

    asyncio.run(delete_task_main(corresponded_id))
    asyncio.run(list_tasks_main())


async def delete_task_main(_id: int):
    try:
        deleted = await delete_todo_by_id(todo_manager, _id)
        if deleted:
            console.print(f"[green]Task with ID {_id} deleted successfully![/green]")
        else:
            console.print(f"[yellow]No task found with ID {_id}.[/yellow]")
    except Exception as e:
        console.print(f"[red]Failed to delete task: {e}[/red]")


@app.command('update', short_help='Update a task by ID')
def update_task(task_id: int, new_name: str):
    corresponded_id = asyncio.run(get_id_by_order_number(todo_manager, int(task_id)))
    logger.debug(f"Corresponded id: {corresponded_id}")

    asyncio.run(update_task_main(task_id, new_name))
    asyncio.run(list_tasks_main())


async def update_task_main(_id: int, new_name: str):
    try:
        if not new_name:
            console.print("[red]Error: Task name cannot be empty.[/red]")
            return

        updated = await update_todo_by_id(todo_manager, _id, new_name)
        if updated:
            console.print(f"[green]Task with ID {_id} updated successfully![/green]")
        else:
            console.print(f"[yellow]No task found with ID {_id}.[/yellow]")
    except Exception as e:
        console.print(f"[red]Failed to update task: {e}[/red]")

@app.command('done', short_help='Set status: Done')
def set_task_done(task_id: int):
    corresponded_id = asyncio.run(get_id_by_order_number(todo_manager, int(task_id)))
    logger.debug(f"Corresponded id: {corresponded_id}")

    asyncio.run(set_task_done_main(task_id))
    asyncio.run(list_tasks_main())


async def set_task_done_main(_id: int):
    try:
        status = await set_status(todo_manager, _id, Status.DONE)
        if status:
            console.print(f"[green]Task with ID {_id} set to Done successfully![/green]")
        else:
            console.print(f"[yellow]No task found with ID {_id}.[/yellow]")
    except Exception as e:
        console.print(f"[red]Failed to set task status: {e}[/red]")
    
if __name__ == '__main__':
    setup_logging()
    app()
