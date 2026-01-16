"""Simple hello command for testing"""
import typer
from rich.console import Console

console = Console()

def hello(name: str = typer.Argument("World")):
    """Say hello."""
    console.print(f"Hello, {name}!")
