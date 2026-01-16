"""
Brew: shell - Natural language to shell commands
Uses Groq's GPT-OSS-120B for intelligent command generation

Usage:
  ant shell find large files
  ant shell compress all images
  ant shell delete node_modules
  ant shell show git history for main.py
"""
import os
import subprocess
from typing import Optional, List
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from groq import Groq

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import GROQ_API_KEY
from auth import get_session

console = Console()

SYSTEM_PROMPT = """You are a shell command expert for macOS/Linux.

Given a natural language request, generate the EXACT shell command(s) to execute.

RULES:
1. Output ONLY the command(s), nothing else
2. If multiple commands needed, use && or ; to chain them
3. Use safe commands (no rm -rf / etc unless specifically asked)
4. Prefer common tools (find over fd, grep over rg) for compatibility
5. Add --no-pager or | cat for git commands
6. For destructive operations, prefer interactive flags (-i)

EXAMPLES:
User: find all python files larger than 1MB
Output: find . -name "*.py" -size +1M

User: show disk usage by folder
Output: du -sh */ | sort -hr | head -20

User: compress all images in current folder
Output: for f in *.{jpg,jpeg,png}; do sips -Z 1920 "$f"; done

User: delete all node_modules folders
Output: find . -name "node_modules" -type d -prune -exec rm -rf {} +

User: show git history for a file
Output: git --no-pager log --oneline -20 -- filename

Output ONLY the command. No explanations. No markdown."""


def shell(args: Optional[List[str]] = typer.Argument(None)):
    """Convert natural language to shell commands."""
    
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    if not args:
        console.print("[yellow]Usage: ant shell <what you want to do>[/yellow]")
        console.print("[dim]Examples:[/dim]")
        console.print("  ant shell find large files")
        console.print("  ant shell compress all images")
        console.print("  ant shell show git history for main.py")
        return
    
    query = " ".join(args)
    
    console.print(f"[dim]Query: {query}[/dim]\n")
    console.print("[cyan]Generating command...[/cyan]\n")
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        # Get current directory context
        cwd = os.getcwd()
        
        # List files for context
        try:
            files = os.listdir(cwd)[:20]
            file_context = ", ".join(files)
        except:
            file_context = "unknown"
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Current directory: {cwd}\nFiles: {file_context}\n\nRequest: {query}"}
            ],
            reasoning_effort="low",
            temperature=0.2,
            max_tokens=500
        )
        
        command = response.choices[0].message.content.strip()
        
        # Clean up any markdown code blocks
        if command.startswith("```"):
            lines = command.split('\n')
            command = '\n'.join(lines[1:-1] if lines[-1].startswith('```') else lines[1:])
        command = command.strip('`').strip()
        
        console.print(Panel(command, title="Generated Command", border_style="cyan"))
        
        # Ask for confirmation
        if Confirm.ask("\nExecute this command?"):
            console.print("\n[dim]Running...[/dim]\n")
            
            # Execute the command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=cwd
            )
            
            if result.stdout:
                console.print(result.stdout)
            
            if result.stderr:
                console.print(f"[yellow]{result.stderr}[/yellow]")
            
            if result.returncode == 0:
                console.print("\n[green]Done[/green]")
            else:
                console.print(f"\n[red]Exit code: {result.returncode}[/red]")
        else:
            console.print("[dim]Command not executed. Copy it manually if needed.[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

# FUNCTION: shell
