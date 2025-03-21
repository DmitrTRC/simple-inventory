from unicodedata import category

import typer
from rich.console import Console
from rich.table import Table

from model.todo_model import Todo, Category

console = Console()

app = typer.Typer()

todos = [
    Todo('Buy groceries'),
    Todo('Complete Python project'),
    Todo('Go for a run')
]


@app.command('new', short_help='Create a new task')
def create_task(name: str, cat: str = 'BACKLOG'):
    if cat.upper() not in Category.__members__:
        console.print(
            f"[red]Error: '{cat}' is not a valid category. Valid options are: {', '.join(Category.__members__.keys())}[/red]")
        return

    cat = Category[cat.upper()]
    todos.append(Todo(name, category=cat))
    console.print(f"Task '{name}' created successfully!")
    list_tasks()


@app.command('list', short_help='List all tasks')
def list_tasks():
    table = Table(title="To-Do List")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    table.add_column("Category", style="green")
    table.add_column("Date Added", style="yellow")
    table.add_column("Date Completed", style="blue")
    table.add_column("Status", style="red")

    for todo_item in todos:
        table.add_row(
            str(todo_item.position),
            todo_item.task,
            str(todo_item.category.name),
            str(todo_item.date_added) if todo_item.date_added else "N/A",
            str(todo_item.date_completed) if todo_item.date_completed else "N/A",
            str(todo_item.status.name),

        )

    console.print(table)


@app.command('del', short_help='Delete a task by ID')
def delete_task(task_id: int):
    if 0 < task_id <= len(todos):
        removed_task = todos.pop(task_id - 1)
        console.print(f"Task '{removed_task}' deleted successfully!")
        list_tasks()
    else:
        console.print("Invalid task ID!")


@app.command('update', short_help='Update a task by ID')
def update_task(task_id: int, new_name: str):
    if 0 < task_id <= len(todos):
        todos[task_id - 1].task = new_name
        console.print(f"Task #{task_id} updated to '{new_name}' successfully!")
        list_tasks()
    else:
        console.print("Invalid task ID!")


if __name__ == '__main__':
    app()
