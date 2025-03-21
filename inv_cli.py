import typer
from rich.console import Console
from rich.table import Table

console = Console()

app = typer.Typer()

todos = [
    "Buy groceries",
    "Complete Python project",
    "Go for a run"
]


@app.command('new', short_help='Create a new task')
def create_task(name: str):
    todos.append(name)
    console.print(f"Task '{name}' created successfully!")


@app.command('list', short_help='List all tasks')
def list_tasks():
    table = Table(title="To-Do List")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Task", style="magenta")
    for idx, task in enumerate(todos, 1):
        table.add_row(str(idx), task)
    console.print(table)


@app.command('del', short_help='Delete a task by ID')
def delete_task(task_id: int):
    if 0 < task_id <= len(todos):
        removed_task = todos.pop(task_id - 1)
        console.print(f"Task '{removed_task}' deleted successfully!")
    else:
        console.print("Invalid task ID!")


@app.command('update', short_help='Update a task by ID')
def update_task(task_id: int, new_name: str):
    if 0 < task_id <= len(todos):
        todos[task_id - 1] = new_name
        console.print(f"Task #{task_id} updated to '{new_name}' successfully!")
    else:
        console.print("Invalid task ID!")


if __name__ == '__main__':
    app()
