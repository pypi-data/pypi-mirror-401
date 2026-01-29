from rich.console import Console
from rich.table import Table

console = Console()


def print_json(data: dict | list) -> None:
    console.print_json(data=data)


def print_error(message: str, json_output: bool = False) -> None:
    if json_output:
        print_json({"error": message})
    else:
        console.print(f"[red]Error: {message}[/red]")


def print_success(message: str, json_output: bool = False) -> None:
    if json_output:
        print_json({"status": "success", "message": message})
    else:
        console.print(f"[green]{message}[/green]")


def print_warning(message: str, json_output: bool = False) -> None:
    if json_output:
        pass
    else:
        console.print(f"[yellow]{message}[/yellow]")


def print_info(message: str, json_output: bool = False) -> None:
    if json_output:
        pass
    else:
        console.print(f"[cyan]{message}[/cyan]")


def output(data: dict | list | str, json_output: bool = False) -> None:
    if json_output:
        if isinstance(data, str):
            print_json({"message": data})
        else:
            print_json(data)
    else:
        if isinstance(data, str):
            console.print(data)
        elif isinstance(data, list):
            for item in data:
                console.print(item)
        else:
            for key, value in data.items():
                console.print(f"[bold]{key}:[/bold] {value}")


def print_table(
    columns: list[tuple[str, str]],
    rows: list[list[str]],
    data: list[dict],
    json_output: bool = False,
    title: str | None = None,
) -> None:
    if json_output:
        print_json(data)
        return

    table = Table(title=title, show_header=True)
    for col_name, col_style in columns:
        table.add_column(col_name, style=col_style)

    for row in rows:
        table.add_row(*row)

    console.print(table)
