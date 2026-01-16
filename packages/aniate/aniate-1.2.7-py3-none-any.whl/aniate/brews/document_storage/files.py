"""
Files Command - List all files in cloud storage
"""
import os
from rich.console import Console
from rich.table import Table
from supabase import create_client

import sys
# Package imports

from aniate.config import SUPABASE_URL, SUPABASE_KEY
from aniate.auth import get_session

console = Console()

def list_files():
    """List all files in cloud storage."""
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    # Create Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    
    user_id = session['user_id']
    
    try:
        result = supabase.table("user_files").select("*").eq("user_id", user_id).order("uploaded_at", desc=True).execute()
        
        if not result.data:
            console.print("[dim]No files in cloud storage[/dim]")
            return
        
        # Calculate totals
        total_size = sum(f['file_size'] for f in result.data)
        total_count = len(result.data)
        
        # Create table
        table = Table(title=f"Cloud Files ({total_count} files, {_format_size(total_size)} total)")
        table.add_column("Filename", style="cyan")
        table.add_column("Size", style="white")
        table.add_column("Type", style="dim")
        table.add_column("Uploaded", style="dim")
        
        for file in result.data:
            size = _format_size(file['file_size'])
            mime = file['mime_type'].split('/')[-1] if file['mime_type'] else 'unknown'
            date = file['uploaded_at'][:10]  # Just the date
            table.add_row(file['filename'], size, mime, date)
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error listing files:[/red] {e}")

def _format_size(bytes_size):
    """Format bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"
