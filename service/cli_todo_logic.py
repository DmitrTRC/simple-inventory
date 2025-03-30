import asyncio

from rich.console import Console
from rich.table import Table

from lazy_orm.db_manager import DatabaseManager
from model.todo_model import Category, Todo, Status
from service.todo_srv import add_todo, get_all_todos, get_id_by_order_number, logger, delete_todo_by_id, \
    update_todo_by_id, set_status

console = Console()

# Constants
TODOS_DB_NAME = 'todos'
todo_manager = DatabaseManager(TODOS_DB_NAME)




# Utility function to validate category
def validate_category(cat: str) -> Category:
    if not cat or cat.upper() not in Category.__members__:
        error_msg = f"'{cat}' is not a valid category. Valid options are: {', '.join(Category.__members__.keys())}"
        console.print(f"[red]Error: {error_msg}[/red]")
        raise ValueError(error_msg)
    return Category[cat.upper()]


# Display tasks in a formatted table
def display_tasks(todos):
    if not todos:
        console.print("[yellow]No tasks found![/yellow]")
        return
    table = Table(title="To-Do List")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Date Added", style="yellow")
    table.add_column("Date Completed", style="blue")
    table.add_column("Status", style="green", justify="center", min_width=10)

    for represent_number, todo_item in enumerate(todos, start=1):
        table.add_row(
            str(represent_number),
            str(todo_item.get('task', "N/A")),
            str(todo_item.get('category', "N/A")),
            str(todo_item.get('date_added', "N/A")),
            str(todo_item.get('date_completed', "N/A")),
            'Completed' if todo_item.get('status') == '1' else '📌'
        )
    console.print(table)


async def create_task_main(name: str, cat: str):
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
    try:
        todos = await get_all_todos(todo_manager)
        display_tasks(todos)
    except Exception as e:
        console.print(f"[red]Failed to fetch tasks: {e}[/red]")


async def delete_task_main(task_id: int):
    try:
        corresponded_id = await get_id_by_order_number(todo_manager, task_id)
        logger.debug(f"Corresponded id: {corresponded_id}")
        deleted = await delete_todo_by_id(todo_manager, corresponded_id)
        if deleted:
            console.print(f"[green]Task with ID {task_id} deleted successfully![/green]")
        else:
            console.print(f"[yellow]No task found with ID {task_id}.[/yellow]")
        await list_tasks_main()
    except Exception as e:
        console.print(f"[red]Failed to delete task: {e}[/red]")


async def update_task_main(task_id: int, new_name: str):
    if not new_name.strip():
        console.print("[red]Error: Task name cannot be empty.[/red]")
        return
    try:
        corresponded_id = await get_id_by_order_number(todo_manager, task_id)
        logger.debug(f"Corresponded id: {corresponded_id}")
        updated = await update_todo_by_id(todo_manager, corresponded_id, new_name)
        if updated:
            console.print(f"[green]Task with ID {task_id} updated successfully![/green]")
        else:
            console.print(f"[yellow]No task found with ID {task_id}.[/yellow]")
        await list_tasks_main()
    except Exception as e:
        console.print(f"[red]Failed to update task: {e}[/red]")


async def set_done_main(task_id: int):
    try:
        corresponded_id = await get_id_by_order_number(todo_manager, task_id)
        logger.debug(f"Corresponded id: {corresponded_id}")
        status = await set_status(todo_manager, corresponded_id, Status.DONE)
        if status:
            console.print(f"[green]Task with ID {task_id} marked as Done![/green]")
        else:
            console.print(f"[yellow]No task found with ID {task_id}.[/yellow]")
        await list_tasks_main()
    except Exception as e:
        console.print(f"[red]Failed to mark task as done: {e}[/red]")
