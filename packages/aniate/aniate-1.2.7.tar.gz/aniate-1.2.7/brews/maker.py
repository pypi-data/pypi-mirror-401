"""
Brew Maker - AI-powered command generator using reasoning model
Uses Groq's OpenAI GPT-OSS-120B for intelligent code generation
"""
import os
from typing import Optional
import typer
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.panel import Panel
from groq import Groq
from pathlib import Path

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import GROQ_API_KEY

console = Console()

SYSTEM_CONTEXT = """You are a Python code generator for the Aniate CLI system.

CONTEXT:
- Aniate is a terminal-based CLI tool built with Python, Typer, and Rich
- Uses Supabase for auth and database (PostgreSQL)
- Uses Groq API for LLM inference
- Files are organized in /brews/<category>/<command>.py

AVAILABLE INFRASTRUCTURE:
1. Supabase:
   - SUPABASE_URL and SUPABASE_KEY from config.py
   - Auth via get_session() from auth.py returns {user_id, access_token, refresh_token}
   - supabase.table("table_name").select/insert/update/delete

2. LLM:
   - SERVER_URL from config.py (FastAPI endpoint)
   - POST to SERVER_URL with {"messages": [...]} returns {"output": str}

3. Secrets:
   - Users can store API keys with ant secrets.add <name> <value>
   - Access via supabase.rpc('get_secret', {'p_user_id': user_id, 'p_name': name})

4. Cloud Storage:
   - Bucket: user-files in Supabase Storage
   - Path: {user_id}/{filename}

TEMPLATE STRUCTURE:
```python
import os
from typing import Optional
import typer
from rich.console import Console
from supabase import create_client

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from config import SUPABASE_URL, SUPABASE_KEY, SERVER_URL
from auth import get_session

console = Console()

def command_name(arg: str = typer.Argument(...)):
    session = get_session()
    if not session:
        console.print("[red]Login required[/red]")
        return
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    
    # Implementation here
```

RULES:
- Write clean, minimal code
- No emojis in output
- Use Rich for terminal output
- Handle errors gracefully
- Use type hints
- Include docstring
- Return the function name at the end in a comment like: # FUNCTION: command_name
"""


def brew_make(prompt: str = typer.Argument(None, help="Describe the command you want")):
    """Generate a new brew using AI reasoning model or load from .py file."""
    
    if not prompt:
        prompt = Prompt.ask("Describe the command you want to create (or path to .py file)")
    
    if not prompt.strip():
        console.print("[red]Please provide a description or file path[/red]")
        return
    
    # Check if prompt ends with .py - could be a file
    if prompt.endswith('.py'):
        file_path = Path(prompt).expanduser()
        
        # If not found, search common locations
        if not file_path.exists():
            search_locations = [
                Path.cwd() / prompt,  # Current directory
                Path.home() / "Desktop" / prompt,  # Desktop
                Path.home() / "Downloads" / prompt,  # Downloads
                Path.home() / prompt,  # Home directory
            ]
            
            for location in search_locations:
                if location.exists() and location.is_file():
                    file_path = location
                    break
            
            if not file_path.exists():
                console.print(f"[red]File not found:[/red] {prompt}")
                console.print(f"[dim]Searched in: current dir, Desktop, Downloads, home[/dim]")
                return
        
        # Load existing Python file
        console.print(f"[dim]Loading brew from {file_path}...[/dim]\n")
        
        try:
            code = file_path.read_text()
            
            # Display code
            console.print("[bold]Loaded Code:[/bold]\n")
            syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
            console.print(syntax)
            
            # Extract function name
            func_name = None
            for line in code.split('\n'):
                if line.strip().startswith('def '):
                    func_name = line.split('def ')[1].split('(')[0]
                    break
            
            if not func_name:
                func_name = Prompt.ask("\nEnter command name")
            
            # Confirm save
            if Confirm.ask(f"\nSave as 'ant {func_name}'?"):
                category = "custom"
                brews_dir = Path(__file__).parent.parent
                category_dir = brews_dir / category
                category_dir.mkdir(exist_ok=True)
                
                dest_path = category_dir / f"{func_name}.py"
                dest_path.write_text(code)
                
                # Update __init__.py
                init_path = category_dir / "__init__.py"
                if not init_path.exists():
                    init_path.write_text(f'from .{func_name} import {func_name}\n\n__all__ = ["{func_name}"]\n')
                else:
                    init_content = init_path.read_text()
                    if func_name not in init_content:
                        init_path.write_text(f'{init_content}from .{func_name} import {func_name}\n')
                
                console.print(f"\n[green]Brew saved: {dest_path}[/green]")
                console.print(f"[dim]Register in main.py to use 'ant {func_name}'[/dim]")
            else:
                console.print("[yellow]Brew discarded[/yellow]")
            
            return
            
        except Exception as e:
            console.print(f"[red]Error loading file:[/red] {e}")
            return
    
    # AI generation path
    console.print("[dim]Generating brew with reasoning model...[/dim]\n")
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        full_response = ""
        
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": SYSTEM_CONTEXT},
                {"role": "user", "content": f"Create a brew command for: {prompt}\n\nReturn ONLY the Python code, no markdown, no explanation."}
            ],
            temperature=0.7,
            max_completion_tokens=4096,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None
        )
        
        # Silently collect response
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            full_response += content
        
        # Extract code
        code = full_response.strip()
        if code.startswith("```python"):
            code = code[9:]
        if code.startswith("```"):
            code = code[3:]
        if code.endswith("```"):
            code = code[:-3]
        code = code.strip()
        
        # Display formatted code once
        console.print("\n[bold]Generated Code:[/bold]\n")
        syntax = Syntax(code, "python", theme="monokai", line_numbers=True)
        console.print(syntax)
        
        # Extract function name
        func_name = None
        for line in code.split('\n'):
            if '# FUNCTION:' in line:
                func_name = line.split('# FUNCTION:')[1].strip()
                break
            elif line.strip().startswith('def '):
                func_name = line.split('def ')[1].split('(')[0]
        
        if not func_name:
            func_name = Prompt.ask("\nEnter command name")
        
        # Use custom folder by default
        category = "custom"
        
        # Confirm save
        if Confirm.ask(f"\nSave as 'ant {func_name}'?"):
            # Create category folder if needed
            brews_dir = Path(__file__).parent.parent
            category_dir = brews_dir / category
            category_dir.mkdir(exist_ok=True)
            
            # Save file
            file_path = category_dir / f"{func_name}.py"
            file_path.write_text(code)
            
            # Create __init__.py if needed
            init_path = category_dir / "__init__.py"
            if not init_path.exists():
                init_path.write_text(f'from .{func_name} import {func_name}\n\n__all__ = ["{func_name}"]\n')
            else:
                # Append to existing init
                init_content = init_path.read_text()
                if func_name not in init_content:
                    init_path.write_text(f'{init_content}from .{func_name} import {func_name}\n')
            
            console.print(f"\n[green]Brew saved: {file_path}[/green]")
            console.print(f"[dim]Register in main.py to use 'ant {func_name}'[/dim]")
        else:
            console.print("[yellow]Brew discarded[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
