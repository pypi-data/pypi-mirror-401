"""
Brew: review - AI code reviewer
Uses Groq's GPT-OSS-120B for intelligent code review

Usage:
  ant review file.py           - Review a file
"""
import os
from typing import Optional, List
import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from groq import Groq
from pathlib import Path

import sys
# Package imports

from aniate.config import GROQ_API_KEY
from aniate.auth import get_session

console = Console()

SYSTEM_PROMPT = """You are a senior code reviewer. Review the code for:

1. SECURITY - vulnerabilities, injection risks, auth issues
2. PERFORMANCE - inefficiencies, N+1 queries, memory leaks
3. BUGS - logic errors, edge cases, race conditions
4. STYLE - readability, naming, structure
5. BEST PRACTICES - patterns, typing, error handling

FORMAT:
## Security
<issues or "None found">

## Performance  
<issues or "None found">

## Bugs
<issues or "None found">

## Style
<suggestions>

## Verdict
<APPROVE / REQUEST CHANGES / NEEDS DISCUSSION>
<one line summary>

Be direct. Be helpful. Terminal output."""


def review(args: Optional[List[str]] = typer.Argument(None)):
    """Review code for security, performance, bugs and style."""
    
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    if not args:
        console.print("[yellow]Usage: ant review file.py[/yellow]")
        return
    
    # First arg is the file
    file_arg = args[0].lstrip('@')  # Remove @ if present
    
    # Find the file
    path = Path(file_arg).expanduser()
    
    if not path.exists():
        search_locations = [
            Path.cwd() / file_arg,
            Path.home() / "Desktop" / file_arg,
            Path.home() / "Downloads" / file_arg,
            Path.home() / file_arg,
        ]
        
        for loc in search_locations:
            if loc.exists():
                path = loc
                break
    
    if not path.exists():
        console.print(f"[red]File not found:[/red] {file_arg}")
        return
    
    code = path.read_text()
    console.print(f"[dim]Reviewing: {path}[/dim]\n")
    
    # Detect language
    ext = path.suffix.lower()
    lang_map = {
        '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
        '.go': 'go', '.rs': 'rust', '.java': 'java', '.cpp': 'cpp',
        '.c': 'c', '.rb': 'ruby', '.php': 'php', '.swift': 'swift'
    }
    lang = lang_map.get(ext, 'text')
    
    # Show code preview
    lines = code.split('\n')
    if len(lines) > 30:
        preview = '\n'.join(lines[:30]) + f"\n... ({len(lines)} lines total)"
    else:
        preview = code
    
    syntax = Syntax(preview, lang, theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=str(path.name), border_style="blue"))
    
    console.print("\n[dim]analyzing...[/dim]\n")
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Review this {lang} code:\n\n```{lang}\n{code}\n```"}
            ],
            reasoning_effort="medium",
            temperature=0.3,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        
        # Color the verdict
        if "APPROVE" in result:
            border = "green"
        elif "REQUEST CHANGES" in result:
            border = "yellow"
        else:
            border = "cyan"
        
        console.print(Panel(result, title="Code Review", border_style=border))
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

# FUNCTION: review
