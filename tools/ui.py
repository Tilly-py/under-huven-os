import time

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


LOGO = r"""
 _   _           _             _   _
| | | |_ __   __| | ___ _ __  | | | |_   ___   _____ _ __
| | | | '_ \ / _` |/ _ \ '__| | |_| | | | \ \ / / _ \ '_ \
| |_| | | | | (_| |  __/ |    |  _  | |_| |\ V /  __/ | | |
 \___/|_| |_|\__,_|\___|_|    |_| |_|\__,_| \_/ \___|_| |_|

                              O S
"""


def print_logo_animated(delay: float = 0.002) -> None:
    """Prints the ASCII logo with a retro terminal animation."""

    for line in LOGO.splitlines():
        for char in line:
            console.print(
                char,
                end="",
                style="bold amber",
                highlight=False,
            )
            time.sleep(delay)

        console.print()


def show_header(animated: bool = False) -> None:
    """Shows the Under Huven OS header."""

    console.clear()

    if animated:
        print_logo_animated()
    else:
        console.print(LOGO, style="bold cyan", highlight=False)

    status = Text()
    status.append(" CPU ", style="bold red")
    status.append("●", style="red")
    status.append("   RAM ", style="bold green")
    status.append("●", style="green")
    status.append("   DISK ", style="bold magenta")
    status.append("●", style="magenta")
    status.append("   PROCESSER ", style="bold yellow")
    status.append("●", style="yellow")

    subtitle = Text(
        "UNDER HUVEN WORKSHOP",
        style="dim bright_white",
    )

    console.print(
        Panel(
            Group(status, subtitle),
            border_style="cyan",
            padding=(0, 2),
        )
    )


def show_menu() -> None:
    """Shows the main menu."""

    table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
        expand=True,
    )

    table.add_column(
        "Val",
        style="bold yellow",
        width=6,
        no_wrap=True,
    )

    table.add_column(
        "Funktion",
        style="bold bright_white",
        width=24,
    )

    table.add_column(
        "Beskrivning",
        style="dim",
    )

    table.add_row(
        "[1]",
        "LIVE DASHBOARD",
        "Övervaka CPU, RAM och disk i realtid",
    )

    table.add_row(
        "[2]",
        "EXPERIMENT MODE",
        "Kör CPU-, RAM- och diskexperiment",
    )

    table.add_row(
        "[3]",
        "SYSTEM INFO",
        "Visa hårdvara och operativsystem",
    )

    table.add_row(
        "[4]",
        "CPU STATUS",
        "Visa aktuell processorbelastning",
    )

    table.add_row(
        "[5]",
        "MEMORY STATUS",
        "Visa aktuell minnesanvändning",
    )

    table.add_row(
        "[6]",
        "DISK STATUS",
        "Visa information om lagringen",
    )

    table.add_row(
        "[7]",
        "SHUTDOWN",
        "Avsluta Under Huven OS",
    )

    console.print(
        Panel(
            table,
            title="[bold cyan] SYSTEM MENU [/bold cyan]",
            subtitle="[dim]Välj modul med 1–7[/dim]",
            border_style="bright_blue",
            padding=(1, 1),
        )
    )

    console.print(
        "[dim cyan]"
        "────────────────────────────────────────────────────────────"
        "[/dim cyan]"
    )


def print_success(message: str) -> None:
    console.print(f"[bold green] [ OK ] [/bold green] {message}")


def print_error(message: str) -> None:
    console.print(
        Panel(
            f"[bold red]{message}[/bold red]",
            title="[bold red] ERROR [/bold red]",
            border_style="red",
            padding=(0, 2),
        )
    )


def print_info(message: str) -> None:
    console.print(f"[bold cyan] [ INFO ] [/bold cyan] {message}")
