import typer
from aiohttp.web_routedef import delete
from rich.console import Console
from rich.table import Table

from lazy_orm.db_manager import DatabaseManager
from model.todo_model import Todo, Category, Status
from service.todo_srv import add_todo, get_all_todos

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

    for todo_item in todos:
        table.add_row(
            str(todo_item.get('id', "Unknown")),
            str(todo_item.get('task', "N/A")),
            str(todo_item.get('category', "N/A")),
            str(todo_item.get('date_added', "N/A")),
            str(todo_item.get('date_completed', "N/A")),
            '✅' if todo_item.get('status') == 1 else '📌'
        )

    console.print(table)


@app.command('del', short_help='Delete a task by ID')
def delete_task(task_id: int):
    asyncio.run(delete_task_main(task_id))


async def delete_task_main(_id: int):
    pass


@app.command('update', short_help='Update a task by ID')
def update_task(task_id: int, new_name: str):
    asyncio.run(update_task_main(task_id, new_name))


async def update_task_main(_id: int, new_name: str):
    pass


if __name__ == '__main__':
    app()
