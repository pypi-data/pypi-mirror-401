# Aniate Brews System - Complete Guide

## Overview

Brews are modular, reusable commands that extend Aniate's functionality. Think of them as plugins you can create, share, and run from any terminal.

## Directory Structure

```
Shell/
├── brews/                   # Core system brews
│   ├── document_storage/    # ant save, fetch, files
│   ├── secrets/             # ant secrets.*
│   └── maker.py             # AI brew generator
├── game/                    # AI-generated brews
│   └── guess.py             # ant guess (AI made this!)
├── custom/                  # Your manual brews
│   └── timer.py             # ant timer (you made this!)
└── main.py                  # Register commands here
```

## Creating Brews

### Method 1: AI Generation (`ant brew.cmd`)

Let AI write the code for you:

```bash
ant brew.cmd "a command that does X"
```

Example:
```bash
ant brew.cmd "a simple number guessing game"
```

AI will:
1. Generate Python code using reasoning model
2. Show you the code with syntax highlighting
3. Ask for category (e.g., "game", "tools", "custom")
4. Save to `<category>/<name>.py`

Then register in main.py (see below).

### Method 2: Manual Creation

1. **Create your Python file:**

```python
# custom/timer.py
import os
import time
import typer
from rich.console import Console

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
    
    console.print(f"Starting {seconds} second timer...")
    for i in range(seconds, 0, -1):
        console.print(f"{i}...")
        time.sleep(1)
    console.print("[green]Time's up![/green]")
```

2. **Create `__init__.py` in folder:**

```python
# custom/__init__.py
from .timer import timer
__all__ = ['timer']
```

3. **Register in `main.py`:**

```python
# Add import at top
from custom.timer import timer

# Register command (after other app.command lines)
app.command(name="timer")(timer)

# Add to SYSTEM_COMMANDS list
SYSTEM_COMMANDS = [..., "timer", ...]
```

4. **Use it:**

```bash
ant timer 30
```

### Method 3: Fetch and Run

Upload your brew to cloud, use on any machine:

```bash
# On Machine A - upload your brew
ant save custom/timer.py

# On Machine B - download and use
ant fetch timer.py
mv ~/Desktop/timer.py custom/
# Register in main.py, then:
ant timer 30
```

## Using Secrets in Brews

Access stored API keys in your code:

```python
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY
from auth import get_session

def my_command():
    session = get_session()
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    
    # Get API key from secrets
    api_key = supabase.rpc('get_secret', {
        'p_user_id': session['user_id'],
        'p_name': 'my_api_key'
    }).execute().data
    
    # Use the API key
    ...
```

## Using LLM in Brews

Call the inference server:

```python
import requests
from config import SERVER_URL

def my_command(prompt: str):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    response = requests.post(SERVER_URL, json={"messages": messages})
    output = response.json()["output"]
    
    console.print(output)
```

## Available Infrastructure

### Config Variables
- `SUPABASE_URL` - Database URL
- `SUPABASE_KEY` - API key
- `SERVER_URL` - LLM endpoint
- `GROQ_API_KEY` - Groq API key
- `SERPER_API_KEY` - Google search API

### Database Tables
- `profiles` - User data
- `assistants` - Chat assistants
- `sessions` - Chat history
- `user_files` - File metadata
- `user_secrets` - Encrypted secrets

### Storage Buckets
- `user-files` - Cloud file storage

### Auth Functions
- `get_session()` - Returns `{user_id, access_token, refresh_token}`
- `save_session(data)` - Persists session

## Best Practices

1. **Always check login**: Start with `get_session()` check
2. **Handle errors**: Wrap Supabase calls in try/except
3. **Use Rich**: For clean terminal output
4. **Type hints**: Use typer arguments properly
5. **Docstrings**: Document your command
6. **No emojis**: Keep output clean and professional

## Sharing Brews

1. Upload your brew: `ant save my_brew.py`
2. Share the filename with others
3. They fetch: `ant fetch my_brew.py`
4. Register in their main.py

Future: Marketplace with UUID-based discovery and ratings.
