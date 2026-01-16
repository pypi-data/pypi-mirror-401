"""
Timer Command - Simple countdown timer
This is an example of a user-created brew file
"""
import os
import time
from typing import Optional
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from auth import get_session

console = Console()

def timer(seconds: int = typer.Argument(10, help="Countdown seconds")):
    """Start a countdown timer."""
    session = get_session()
    if not session:
        console.print("[red]Login required[/red]")
        return
    
    console.print(f"[cyan]Starting {seconds} second timer...[/cyan]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}s"),
        console=console
    ) as progress:
        task = progress.add_task("Countdown", total=seconds)
        
        for i in range(seconds):
            time.sleep(1)
            progress.update(task, advance=1)
    
    console.print("\n[green]Time's up![/green]")
