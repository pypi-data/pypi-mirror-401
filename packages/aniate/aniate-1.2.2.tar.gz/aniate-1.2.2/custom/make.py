import os
import subprocess
from typing import Optional

import typer
from rich.console import Console
from supabase import create_client

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import SUPABASE_URL, SUPABASE_KEY
from auth import get_session

console = Console()


def make(
    target: Optional[str] = typer.Argument(
        None, help="Make target to build (default: default target)."
    ),
    cwd: Optional[Path] = typer.Option(
        None,
        "--cwd",
        "-c",
        help="Working directory to run make in. Defaults to current directory.",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    ),
):
    """
    Execute a `make` command in the current (or specified) directory.

    This command requires the user to be logged in. It runs `make` with an optional
    target and prints the output using Rich. Errors from the subprocess are shown
    in red.
    """
    session = get_session()
    if not session:
        console.print("[red]Login required[/red]")
        raise typer.Exit(code=1)

    # Initialise Supabase client (session may be used for analytics later)
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(
        session["access_token"], session.get("refresh_token", "")
    )

    work_dir = cwd or os.getcwd()
    cmd = ["make"]
    if target:
        cmd.append(target)

    try:
        result = subprocess.run(
            cmd,
            cwd=work_dir,
            capture_output=True,
            text=True,
            check=True,
        )
        console.print("[green]Make succeeded:[/green]")
        console.print(result.stdout)
        if result.stderr:
            console.print("[yellow]Warnings:[/yellow]")
            console.print(result.stderr)
    except subprocess.CalledProcessError as e:
        console.print("[red]Make failed:[/red]")
        console.print(e.stdout or "")
        console.print("[red]Error output:[/red]")
        console.print(e.stderr or "")
        raise typer.Exit(code=e.returncode)


# FUNCTION: make