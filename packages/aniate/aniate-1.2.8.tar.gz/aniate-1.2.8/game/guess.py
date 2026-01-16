import os
import random
from typing import Optional

import typer
from rich.console import Console
from rich.prompt import Prompt
from supabase import create_client

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import SUPABASE_URL, SUPABASE_KEY, SERVER_URL
from auth import get_session

console = Console()

def guess():
    """
    Simple number guessing game.
    The user tries to guess a randomly selected integer between 1 and 10.
    """
    session = get_session()
    if not session:
        console.print("[red]Login required[/red]")
        return

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))

    target = random.randint(1, 10)
    try:
        user_input = Prompt.ask("[bold]Guess a number between 1 and 10[/bold]")
        guess_num = int(user_input)
    except ValueError:
        console.print("[red]Invalid input. Please enter an integer.[/red]")
        return

    if guess_num < 1 or guess_num > 10:
        console.print("[red]Number out of range. Must be between 1 and 10.[/red]")
        return

    if guess_num == target:
        console.print("[green]Congratulations! You guessed correctly.[/green]")
    else:
        console.print(f"[yellow]Sorry, the correct number was {target}.[/yellow]")

# FUNCTION: guess