"""
Brew: what - Explain errors in plain English
Uses Groq's llama-3.1-8b-instant for fast error explanation

Usage:
  ant what error.log           - Explain errors in a file
  ant what TypeError: ...      - Explain inline error text
  command 2>&1 | ant what -    - Pipe errors directly
"""
import os
import subprocess
from typing import Optional, List
import typer
from rich.console import Console
from rich.panel import Panel
from groq import Groq
from pathlib import Path

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import GROQ_API_KEY
from auth import get_session

console = Console()

SYSTEM_PROMPT = """You explain programming errors in simple, plain English.

Given an error message or stack trace:
1. What went wrong (one sentence, no jargon)
2. Why it happened (simple explanation)
3. Common causes (bullet points)
4. Quick fix hint

Be extremely concise. Imagine explaining to someone new to programming.
No code in your response - just explanation.
Terminal output format."""


def what(args: Optional[List[str]] = typer.Argument(None)):
    """Explain errors in plain English."""
    
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    error_content = ""
    source = "Error"
    
    if not args:
        console.print("[yellow]Usage:[/yellow]")
        console.print("  ant what error.log           - Explain errors in a file")
        console.print("  ant what 'TypeError: ...'    - Explain inline error")
        console.print("\n[dim]Tip: Pipe errors directly:[/dim]")
        console.print("  python script.py 2>&1 | ant what -")
        return
    
    # Check if reading from stdin (piped input)
    if args[0] == '-':
        import sys as _sys
        if not _sys.stdin.isatty():
            error_content = _sys.stdin.read()
            source = "Piped Input"
        else:
            console.print("[red]No piped input detected[/red]")
            return
    else:
        # First arg could be a file or error text
        first_arg = args[0].lstrip('@')
        
        # Check if it's a file
        path = Path(first_arg).expanduser()
        
        if not path.exists():
            search_locations = [
                Path.cwd() / first_arg,
                Path.home() / "Desktop" / first_arg,
                Path.home() / "Downloads" / first_arg,
            ]
            
            for loc in search_locations:
                if loc.exists():
                    path = loc
                    break
        
        if path.exists() and path.is_file():
            error_content = path.read_text()
            source = str(path.name)
            console.print(f"[dim]Reading: {path}[/dim]\n")
        else:
            # Treat all args as error text
            error_content = " ".join(args)
            source = "Error Text"
    
    if not error_content.strip():
        console.print("[red]No error content found[/red]")
        return
    
    # Show brief preview
    preview = error_content[:400] + "..." if len(error_content) > 400 else error_content
    console.print(Panel(preview, title=source, border_style="red"))
    
    console.print("\n[cyan]Analyzing...[/cyan]\n")
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Explain this error in plain English:\n\n{error_content}"}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        result = response.choices[0].message.content
        
        console.print(Panel(result, title="What Happened", border_style="yellow"))
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

# FUNCTION: what
