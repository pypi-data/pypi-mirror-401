"""
Save Command - Upload files to cloud storage
"""
import os
from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from supabase import create_client
import mimetypes

import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import SUPABASE_URL, SUPABASE_KEY
from auth import get_session

console = Console()

def save_file(filepath: str = typer.Argument(..., help="File to upload"), cloud_name: Optional[str] = typer.Argument(None, help="Custom name in cloud")):
    """Upload a file to cloud storage."""
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    # Resolve file path
    file_path = Path(filepath).expanduser().resolve()
    
    if not file_path.exists():
        console.print(f"[red]File not found:[/red] {filepath}")
        return
    
    if not file_path.is_file():
        console.print(f"[red]Not a file:[/red] {filepath}")
        return
    
    # Get file info
    file_size = file_path.stat().st_size
    filename = cloud_name if cloud_name else file_path.name
    mime_type = mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream'
    
    # Size warning for large files
    if file_size > 10 * 1024 * 1024:  # 10MB
        size_mb = file_size / (1024 * 1024)
        console.print(f"[yellow]Warning: Large file ({size_mb:.1f} MB)[/yellow]")
        confirm = console.input("Continue? (y/n): ")
        if confirm.lower() != 'y':
            console.print("[dim]Upload cancelled[/dim]")
            return
    
    # Create Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    
    user_id = session['user_id']
    storage_path = f"{user_id}/{filename}"
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[cyan]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console
        ) as progress:
            task = progress.add_task(f"Uploading {filename}...", total=100)
            
            # Read file
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            progress.update(task, advance=30)
            
            # Upload to Supabase Storage
            supabase.storage.from_('user-files').upload(
                storage_path,
                file_data,
                file_options={"content-type": mime_type, "upsert": "true"}
            )
            
            progress.update(task, advance=40)
            
            # Save metadata to database
            metadata = {
                "user_id": user_id,
                "filename": filename,
                "storage_path": storage_path,
                "file_size": file_size,
                "mime_type": mime_type
            }
            
            # Upsert (insert or update)
            supabase.table("user_files").upsert(metadata, on_conflict="user_id,filename").execute()
            
            progress.update(task, advance=30)
        
        # Success message
        size_str = _format_size(file_size)
        console.print(f"[bold green]✓ Uploaded {filename}[/bold green] [dim]({size_str})[/dim]")
        
    except Exception as e:
        console.print(f"[red]Upload failed:[/red] {e}")

def _format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"
