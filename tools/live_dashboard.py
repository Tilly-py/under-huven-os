import time
import psutil


from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, TextColumn, BarColumn
from tools.byte_formater import bytes_to_gb

console = Console()

def create_usage_bar(label, percent):
    progress = Progress(
        TextColumn(f"[bold cyan]{label}[/bold cyan]"),
        BarColumn(bar_width=30, complete_style="green", finished_style="green", pulse_style="green"),
        TextColumn(f"[bold yellow]{percent}%[/bold yellow]"),
        expand=False
    )

    task = progress.add_task(label, total=100)
    progress.update(task, completed=percent)
    return progress

def get_dashboard():
    cpu_percent = psutil.cpu_percent(interval=None)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    table = Table.grid(expand=True)
    table.add_column(justify="left")
    table.add_column(justify="left")

    table.add_row(
        "[bold cyan]CPU Usage[/bold cyan]",
        create_usage_bar("CPU", cpu_percent)
    )

    table.add_row(
        "[bold green]RAM Usage[/bold green]",
        create_usage_bar("RAM", memory.percent)
    )

    table.add_row(
        "[bold magenta]DISK Usage[/bold magenta]",
        create_usage_bar("DISK", disk.percent)
    )

    info_table = Table(title="System Status", border_style="cyan")

    info_table.add_column("Component", style="bold yellow")
    info_table.add_column("Metric", style="bold white")

    info_table.add_row("CPU Usage", f"{cpu_percent}%")
    info_table.add_row("RAM Total", f"{bytes_to_gb(memory.total)} GB")
    info_table.add_row("RAM Usage", f"{bytes_to_gb(memory.used)} GB")
    info_table.add_row("RAM Available", f"{bytes_to_gb(memory.available)} GB")
    info_table.add_row("Disk Total", f"{bytes_to_gb(disk.total)} GB")
    info_table.add_row("Disk Usage", f"{bytes_to_gb(disk.used)} GB")
    info_table.add_row("Disk Available", f"{bytes_to_gb(disk.free)} GB")

    layout = Table.grid(expand=True)
    layout.add_row(
        Panel.fit(
            "[bold cyan]UNDER HUVEN OS - LIVE DASHBOARD[/bold cyan]\n"
            "[green]Press Ctrl+C to exit[/green]",
            border_style="cyan",
            padding=(1, 4),
        )
    )
    layout.add_row(Panel(table, title="Live System Usage", border_style="green"))
    layout.add_row(info_table)
    return layout

def show_live_dashboard():
    console.clear()

    try:
        with Live(get_dashboard(), refresh_per_second=1, screen=True) as live:
            while True:
                live.update(get_dashboard())
                time.sleep(0.5)
    except KeyboardInterrupt:
        console.clear()
        console.print("[bold red]Exiting Live Dashboard...[/bold red]")