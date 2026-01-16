"""
Brew: fix - AI debugger that fixes code or errors
Uses Groq's GPT-OSS-120B for intelligent analysis and fixing

Usage:
  ant fix file.py              - Fix issues in a file
  ant fix file.py make it work - Fix with specific instructions
  ant fix error.log            - Analyze error log and suggest fix
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

SYSTEM_PROMPT = """You are an expert debugger and code fixer. 

You may receive:
1. A code file with optional instructions to fix it
2. An error log/stack trace to analyze

For CODE FILES:
- Identify issues (bugs, errors, bad patterns)
- Provide the EXACT fixed code
- Explain what you changed

For ERROR LOGS:
- Identify the root cause
- Show the exact fix needed

FORMAT:
## Problem
<one line explanation>

## The Fix
<code with file path, or corrected code>

## What Changed
<bullet points>

Be direct. No fluff. Terminal output."""


def fix(args: Optional[List[str]] = typer.Argument(None)):
    """Fix code or analyze errors using AI."""
    
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    if not args:
        console.print("[yellow]Usage:[/yellow]")
        console.print("  ant fix file.py              - Fix issues in a file")
        console.print("  ant fix file.py make it work - Fix with instructions")
        console.print("  ant fix error.log            - Analyze error log")
        return
    
    # First arg is the file, rest is instructions
    file_arg = args[0].lstrip('@')  # Remove @ if present
    instructions = " ".join(args[1:]) if len(args) > 1 else ""
    
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
        # Treat as error text
        error_text = " ".join(args)
        console.print("[dim]Treating input as error text...[/dim]\n")
        _analyze_error(error_text)
        return
    
    # Read file content
    content = path.read_text()
    console.print(f"[dim]Analyzing: {path}[/dim]\n")
    
    # Detect language
    ext = path.suffix.lower()
    lang_map = {
        '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
        '.go': 'go', '.rs': 'rust', '.java': 'java', '.cpp': 'cpp',
        '.c': 'c', '.rb': 'ruby', '.php': 'php', '.swift': 'swift',
        '.log': 'text', '.txt': 'text', '.md': 'markdown'
    }
    lang = lang_map.get(ext, 'text')
    
    # Check if it's an error log
    is_error_log = ext in ['.log', '.txt'] or 'Traceback' in content or 'Error:' in content
    
    if is_error_log and not instructions:
        _analyze_error(content, str(path))
        return
    
    # Show code preview
    lines = content.split('\n')
    if len(lines) > 25:
        preview = '\n'.join(lines[:25]) + f"\n... ({len(lines)} lines total)"
    else:
        preview = content
    
    syntax = Syntax(preview, lang, theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title=str(path.name), border_style="blue"))
    
    # Build prompt
    if instructions:
        user_prompt = f"Fix this {lang} code. Instructions: {instructions}\n\nCode:\n```{lang}\n{content}\n```"
    else:
        user_prompt = f"Find and fix any issues in this {lang} code:\n\n```{lang}\n{content}\n```"
    
    console.print("\n[dim]analyzing...[/dim]\n")
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            reasoning_effort="medium",
            temperature=0.3,
            max_tokens=3000
        )
        
        result = response.choices[0].message.content
        console.print(Panel(result, title="Fix", border_style="green"))
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


def _analyze_error(error_content: str, source: str = None):
    """Analyze error log and suggest fix."""
    
    preview = error_content[:500] + "..." if len(error_content) > 500 else error_content
    title = source if source else "Error"
    console.print(Panel(preview, title=title, border_style="red"))
    
    console.print("\n[dim]analyzing...[/dim]\n")
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this error and provide the fix:\n\n{error_content}"}
            ],
            reasoning_effort="medium",
            temperature=0.3,
            max_tokens=2000
        )
        
        result = response.choices[0].message.content
        console.print(Panel(result, title="Fix", border_style="green"))
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")

# FUNCTION: fix
