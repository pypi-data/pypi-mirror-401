"""
Fetch Command - Download files from cloud storage
"""
import os
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt
from rich.table import Table
from supabase import create_client

import sys
# Package imports

from aniate.config import SUPABASE_URL, SUPABASE_KEY
from aniate.auth import get_session

console = Console()

def fetch_file(filename: Optional[str] = typer.Argument(None, help="File to download")):
    """Download a file from cloud storage."""
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    # Create Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    
    user_id = session['user_id']
    
    # If no filename provided, show interactive list
    if not filename:
        filename = _select_file_interactive(supabase, user_id)
        if not filename:
            return
    
    # Get file metadata
    try:
        result = supabase.table("user_files").select("*").eq("user_id", user_id).eq("filename", filename).execute()
        
        if not result.data:
            console.print(f"[red]File not found in cloud:[/red] {filename}")
            return
        
        file_meta = result.data[0]
        storage_path = file_meta['storage_path']
        file_size = file_meta['file_size']
        
        # Always save to Desktop
        desktop = Path.home() / "Desktop"
        dest_path = desktop / filename
        
        # Check if file exists locally
        if dest_path.exists():
            overwrite = Prompt.ask(f"[yellow]File exists. Overwrite?[/yellow]", choices=["y", "n"], default="n")
            if overwrite == 'n':
                console.print("[dim]Download cancelled[/dim]")
                return
        
        # Download file
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"Downloading {filename}...", total=100)
            
            # Download from Supabase Storage
            file_data = supabase.storage.from_('user-files').download(storage_path)
            
            progress.update(task, advance=70)
            
            # Write to local file
            with open(dest_path, 'wb') as f:
                f.write(file_data)
            
            progress.update(task, advance=30)
        
        # Success message
        size_str = _format_size(file_size)
        console.print(f"[bold green]✓ Downloaded {filename}[/bold green] [dim]({size_str})[/dim]")
        console.print(f"[dim]Saved to: {dest_path}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Download failed:[/red] {e}")

def _select_file_interactive(supabase, user_id):
    """Show interactive file selector."""
    try:
        result = supabase.table("user_files").select("*").eq("user_id", user_id).order("uploaded_at", desc=True).execute()
        
        if not result.data:
            console.print("[dim]No files in cloud storage[/dim]")
            return None
        
        # Show table
        table = Table(title="Cloud Files")
        table.add_column("#", style="cyan")
        table.add_column("Filename", style="white")
        table.add_column("Size", style="dim")
        table.add_column("Date", style="dim")
        
        for idx, file in enumerate(result.data, 1):
            size = _format_size(file['file_size'])
            date = file['uploaded_at'][:10]  # Just the date
            table.add_row(str(idx), file['filename'], size, date)
        
        console.print(table)
        
        # Prompt for selection
        choice = Prompt.ask("\n[cyan]Select file number (or 'q' to quit)[/cyan]")
        
        if choice.lower() == 'q':
            return None
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(result.data):
                return result.data[idx]['filename']
            else:
                console.print("[red]Invalid selection[/red]")
                return None
        except ValueError:
            console.print("[red]Invalid input[/red]")
            return None
            
    except Exception as e:
        console.print(f"[red]Error listing files:[/red] {e}")
        return None

def _format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"
