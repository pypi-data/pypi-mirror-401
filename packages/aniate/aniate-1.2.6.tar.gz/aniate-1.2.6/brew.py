"""
Brew System - Create and manage custom commands
"""
from rich.console import Console
from pathlib import Path

console = Console()

def brew_cmd(name: str):
    """Brew a custom command template."""
    console.print(f"\n[bold cyan]🍺 Brewing Command: {name}[/bold cyan]\n")
    
    commands_dir = Path(__file__).parent / "commands"
    cmd_file = commands_dir / f"{name}.py"
    
    if cmd_file.exists():
        console.print(f"[yellow]Command '{name}' already exists.[/yellow]")
        return
    
    # Template for custom commands
    template = f'''"""
{name.title()} Command - Custom brewed command
"""
import requests
from rich.console import Console
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import SERVER_URL

console = Console()

def {name}_execute(arg: str):
    """Execute the {name} command."""
    console.print(f"[cyan]{name.title()} command executing:[/cyan] {{arg}}")
    
    # TODO: Implement your command logic here
    # You can use the LLM via SERVER_URL
    # You can access other APIs
    # You can process files, data, etc.
    
    console.print(f"[green]✓ {name.title()} completed[/green]")
'''
    
    try:
        cmd_file.write_text(template)
        console.print(f"[green]✓ Command '{name}' brewed successfully[/green]")
        console.print(f"[dim]Edit: {cmd_file}[/dim]")
        console.print(f"[dim]Use: ant {name} \"your input\"[/dim]\n")
    except Exception as e:
        console.print(f"[red]Brew failed:[/red] {e}")

def delete_cmd(name: str):
    """Delete a custom brewed command."""
    commands_dir = Path(__file__).parent / "commands"
    cmd_file = commands_dir / f"{name}.py"
    
    if not cmd_file.exists():
        console.print(f"[yellow]Command '{name}' not found.[/yellow]")
        return
    
    # Prevent deleting core commands
    core_commands = ['chat', 'net']
    if name in core_commands:
        console.print(f"[red]Cannot delete core command '{name}'[/red]")
        return
    
    try:
        cmd_file.unlink()
        console.print(f"[bold red]✓ Command '{name}' deleted[/bold red]")
    except Exception as e:
        console.print(f"[red]Delete failed:[/red] {e}")
