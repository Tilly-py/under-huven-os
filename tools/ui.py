from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

console = Console()


def show_header():
    title = Text("Under Huven OS", style="bold cyan")
    subtitle = Text("Visualisera CPU, RAM, disk och processer", style="bold green")

    panel = Panel.fit(f"{title}\n{subtitle}", border_style="cyan", padding=(1, 4))
    console.print(panel)


def show_menu():
    table = Table(title="Main Menu", show_header=False, border_style="cyan")

    table.add_column("Val", style="bold yellow")
    table.add_column("Funktion", style="white")

    table.add_row("[1]", "Live dashboard")
    table.add_row("[2]", "Kör experiment")
    table.add_row("[3]", "Systeminformation")
    table.add_row("[4]", "Visa CPU-användning")
    table.add_row("[5]", "Visa minnesanvändning")
    table.add_row("[6]", "Visa diskinformation")
    table.add_row("[7]", "Avsluta")

    console.print(table)


def print_success(message):
    console.print(f"[bold green]✓ {message}[/bold green]")


def print_error(message):
    console.print(f"[bold red]✗ {message}[/bold red]")


def print_info(message):
    console.print(f"[bold cyan]ℹ {message}[/bold cyan]")
