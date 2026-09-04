import json
import shutil
import subprocess
import time
from pathlib import Path

import psutil
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn

from tools.explanations import CPU_EXPLANATION, DISK_EXPLANATION, RAM_EXPLANATION
from tools.visualizer import show_test_intro

console = Console()

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "experiments.json"

EXPLANATIONS = {
    "cpu": CPU_EXPLANATION,
    "ram": RAM_EXPLANATION,
    "disk": DISK_EXPLANATION,
}


def load_experiments() -> dict:
    """
    loads the experiment data from the JSON file.
    """

    with DATA_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def run_stress_command(command: list[str], duration: int) -> None:
    """
    Runs a stress command and shows a progress bar while it is running
    """

    if shutil.which("stress") is None:
        console.print(
            Panel(
                "Kommandot 'stress' saknas. \n\n"
                "Kör ./install.sh eller installera stress med:\n\n"
                "sudo apt install stress",
                title="kan inte köra test",
                border_style="red",
            )
        )
        return

    process = subprocess.Popen(command)

    with Progress(
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=30),
        TextColumn("[bold yellow]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Testet körs", total=duration)

        for _ in range(duration):
            if process.poll() is not None:
                break

            time.sleep(1)
            progress.update(task, advance=1)

        process.wait()
        console.print("\n[bold green]Klart.[\bold green]")


def run_command_experiment(experiment: dict) -> None:
    """
    Runs an experiment that is based on a shell command
    """
    title = experiment["title"]
    explanation_key = experiment["explnation_key"]
    explanation = EXPLANATIONS[explanation_key]
    impacts = experiment["impacts"]
    command = experiment["command"]
    duration = experiment["duration"]
    look_for = experiment["look_for"]

    console.clear()
    console.print(show_test_intro(title, explanation, impacts))
    console.print(f"\n[bold yellow]Titta efter:[/bold yellow]{look_for}\n")

    run_stress_command(command, duration)


def run_disk_experiment(experiment: dict) -> None:
    """
    Writes a temporary file to show disk activity.
    """

    title = experiment["title"]
    explanation_key = experiment["explnation_key"]
    explanation = EXPLANATIONS[explanation_key]
    impacts = experiment["impacts"]
    size_mb = experiment["size_mb"]
    look_for = experiment["look_for"]

    console.clear()
    console.print(show_test_intro(title, explanation, impacts))
    console.print(f"\n[bold yellow]Titta efter:[/bold yellow]{look_for}\n")

    test_file = Path("/tmp/under-huven-disk-test.bin")
    chunk = b"0" * 1024 * 1024

    console.print(f"[bold yellow]Skriver:[/bold yellow] {size_mb} mb till {test_file}")

    try:
        with Progress(
            TextColumn("[bold cyan]{task.description}"),
            BarColumn(bar_width=30),
            TextColumn("[bold yellow] {task.completed:.0f}/{task.total:.0f} MB"),
            console=console,
        ) as progress:
            task = progress.add_task("Skriver testfil", total=size_mb)

            with test_file.open("wb") as file:
                for _ in range(size_mb):
                    file.write(chunk)
                    progress.update(task, advance=1)

        disk = psutil.disk_usage("/")
        console.print("\n[bold green]Klart.[/bold green]")
        console.print(f"Diskanvändning just nu: [bold cyan]{disk.percent}%[/bold cyan]")

    finally:
        if test_file.exists():
            test_file.unlink()
            console.print("[cyan]Testfilen togs bort igen.[/cyan]")


def show_experiment_menu() -> None:
    """
    Shows the experiment menu.
    """

    experiments = load_experiments()

    while True:
        console.clear()
        console.print("[bold cyan]Experimentläge[/bold cyan]\n")
        console.print("[1] CPU-test")
        console.print("[2] RAM-test")
        console.print("[3] Disk-test")
        console.print("[4] Tillbaka")

        choice = input("\nVälj experiment: ").strip()

        if choice == "1":
            run_command_experiment(experiments["cpu"])
        elif choice == "2":
            run_command_experiment(experiments["ram"])
        elif choice == "3":
            run_disk_experiment(experiments["disk"])
        elif choice == "4":
            break
        else:
            console.print("[bold red]Ogiltigt val. Försök igen.[/bold red]")

        input("\nTryck Enter för att fortsätta...")
