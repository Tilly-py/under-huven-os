import json
import shutil
import subprocess
import time
from pathlib import Path
import os

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

    process = subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

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
    console.print("\n[bold green]Klart.[/bold green]")


def run_command_experiment(experiment: dict) -> None:
    """
    Runs an experiment that is based on a shell command
    """
    title = experiment["title"]
    explanation_key = experiment["explanation_key"]
    explanation = EXPLANATIONS[explanation_key]
    impacts = experiment["impacts"]
    duration = experiment["duration"]
    look_for = experiment["look_for"]

    if explanation_key == "cpu":
        cpu_count = psutil.cpu_count(logical=True) or 1
        load_ratio = experiment.get("load_ratio", 0.8)

        workers = max(1, int(cpu_count * load_ratio))

        command = [
            "stress",
            "--cpu",
            str(workers),
            "--timeout",
            str(duration),
        ]
    elif explanation_key == "ram":
        memory = psutil.virtual_memory()

        available_mb = int(memory.available / (1024 * 1024))
        load_ratio = experiment.get("load_ratio", 0.30)
        max_mb = experiment.get("max_mb", 4096)

        ram_mb = max(64, min(int(available_mb * load_ratio), max_mb))

        command = [
            "stress",
            "--vm",
            "1",
            "--vm-bytes",
            f"{ram_mb}M",
            "--vm-keep",
            "--timeout",
            str(duration),
        ]

    else:
        command = experiment("command")

    console.clear()
    console.print(show_test_intro(title, explanation, impacts))

    if explanation_key == "cpu":
        console.print(f"\n[bold cyan]System:[/bold cyan] {cpu_count} CPU-kärnor, ")
        console.print(
            f"[bold cyan]Workers:[/bold cyan] {workers} workers ({load_ratio:.0%})"
        )

    elif explanation_key == "ram":
        console.print(f"\n[bold cyan]Tillgängligt RAM:[/bold cyan] {available_mb} MB")
        console.print(
            f"[bold yellow]Testet reserverar:[/bold yellow] "
            f"{ram_mb} MB ({load_ratio:.0%} av tillgängligt RAM)"
        )
    console.print(f"\n[bold yellow]Titta efter:[/bold yellow]{look_for}\n")

    run_stress_command(command, duration)


def run_disk_experiment(experiment: dict) -> None:
    """
    Writes a temporary file to show disk activity.
    """

    title = experiment["title"]
    explanation_key = experiment["explanation_key"]
    explanation = EXPLANATIONS[explanation_key]
    impacts = experiment["impacts"]

    duration = experiment.get("duration", 15)
    max_mb = experiment.get("max_mb", 1024)
    look_for = experiment["look_for"]

    console.clear()
    console.print(show_test_intro(title, explanation, impacts))
    console.print(f"\n[bold yellow]Titta efter:[/bold yellow] {look_for}\n")

    test_dir = Path.home() / ".under-huven"
    test_dir.mkdir(exist_ok=True)

    test_file = test_dir / "disk-test.bin"

    chunk_size_mb = 4
    chunk = b"0" * (chunk_size_mb * 1024 * 1024)

    disk = psutil.disk_usage(test_dir)
    free_mb = int(disk.free / (1024 * 1024))

    if free_mb < 1024:
        console.print(
            "[bold red]För lite ledigt diskutrymme för disk-testet.[/bold red]"
        )
        return

    target_mb = min(
        max_mb,
        int(free_mb * 0.05),
    )

    console.print(f"[cyan]Ledigt utrymme:[/cyan] {free_mb} MB")
    console.print(f"[yellow]Maximal teststorlek:[/yellow] {target_mb} MB")
    console.print(f"[yellow]Maximal testtid:[/yellow] {duration} sekunder\n")

    io_before = psutil.disk_io_counters()
    start_time = time.perf_counter()

    written_mb = 0

    try:
        with test_file.open("wb") as file:
            with Progress(
                TextColumn("[bold cyan]{task.description}"),
                BarColumn(bar_width=30),
                TextColumn("[bold yellow]{task.completed:.0f}/{task.total:.0f} MB"),
                console=console,
            ) as progress:
                task = progress.add_task(
                    "Skriver till disk",
                    total=target_mb,
                )

                while written_mb < target_mb:
                    elapsed = time.perf_counter() - start_time

                    if elapsed >= duration:
                        break

                    file.write(chunk)

                    written_mb += chunk_size_mb

                    progress.update(
                        task,
                        advance=chunk_size_mb,
                    )

                    if written_mb % 64 == 0:
                        file.flush()
                        os.fsync(file.fileno())

            file.flush()
            os.fsync(file.fileno())

        elapsed = time.perf_counter() - start_time
        io_after = psutil.disk_io_counters()

        speed = written_mb / elapsed if elapsed > 0 else 0

        console.print("\n[bold green]Klart.[/bold green]")
        console.print(f"[cyan]Skrivet:[/cyan] {written_mb} MB")
        console.print(f"[cyan]Tid:[/cyan] {elapsed:.1f} sekunder")
        console.print(f"[cyan]Genomsnittlig skrivhastighet:[/cyan] {speed:.1f} MB/s")

        if io_before and io_after:
            actual_written = (io_after.write_bytes - io_before.write_bytes) / (
                1024 * 1024
            )

            console.print(f"[cyan]Systemets disk-I/O:[/cyan] +{actual_written:.1f} MB")

    finally:
        if test_file.exists():
            test_file.unlink()

        console.print("[dim]Testfilen togs bort igen.[/dim]")


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
