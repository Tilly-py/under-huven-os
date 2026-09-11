from rich.panel import Panel
from rich.table import Table


def impact_bar(level: int) -> str:
    """
    Converts an impact level into a visual bar
    The diffrent levels are the following:
    0 = almost no impact
    1 = small impact
    2 = medium impact
    3 = large impact
    """
    if level == 0:
        return "[dim]░░░░░░░░░░[/dim]"
    elif level == 1:
        return "[green]██░░░░░░░░[/green]"
    elif level == 2:
        return "[yellow]█████░░░░░[/yellow]"
    elif level == 3:
        return "[red]██████████[/red]"
    else:
        return "[dim]??????????[/dim]"


def impact_text(level: int) -> str:
    """
    Converts an impact level into a short explanation
    """
    if level == 0:
        return "Påverkas nästan inte"
    elif level == 1:
        return "påverkas lite"
    elif level == 2:
        return "Påverkas tydligt"
    elif level == 3:
        return "påverkas mycket"
    else:
        return "Okänd påverkan"


def show_component_impact(
    title: str,
    impacts: list[
        tuple[
            str,
            int,
            str,
        ]
    ],
) -> Panel:
    """
    Creates a Rich panel that shows which computer components are affected.

    Example impact structure:

        [
        ("CPU", 3, "Processorn får mycket arbete."),
        ("RAM", 1, "Lite minne används."),
        ("Disk", 0, "Nästan inget skrivs."),
    ]
    """
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan")
    table.add_column("Komponent", style="bold")
    table.add_column("Påverkan")
    table.add_column("Vad händer?")

    for component, level, description in impacts:
        table.add_row(
            component, f"{impact_bar(level)} {impact_text(level)}", description
        )
    return Panel(
        table,
        title=f"[bold cyan]{title}[/bold cyan]",
        border_style="cyan",
    )


def show_test_intro(
    title: str, explanation: str, impacts: list[tuple[str, int, str]]
) -> Panel:
    """
    Creates a panel with a short explanation and a component impact table
    """
    impact_panel = show_component_impact("Komponenter som påverkas", impacts)

    table = Table.grid(expand=True)
    table.add_row(f"[bold]{explanation.strip()}[/bold]")
    table.add_row("")
    table.add_row(impact_panel)

    return Panel(
        table,
        title=f"[bold green]{title}[/bold green]",
        border_style="green",
        padding=(1, 2),
    )
