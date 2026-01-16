"""
Secrets Management - Encrypted storage for API keys and credentials
Uses Supabase Vault for server-side encryption
"""
import os
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from supabase import create_client
import hashlib

import sys
# Package imports

from aniate.config import SUPABASE_URL, SUPABASE_KEY
from aniate.auth import get_session

console = Console()


def add_secret(name: str = typer.Argument(..., help="Secret name (e.g., groq_api)"), 
               value: str = typer.Argument(None, help="Secret value")):
    """Add or update a secret."""
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    if not value:
        value = Prompt.ask(f"Enter value for '{name}'", password=True)
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    
    user_id = session['user_id']
    
    try:
        # Store secret with RPC function that encrypts server-side
        supabase.rpc('store_secret', {
            'p_user_id': user_id,
            'p_name': name,
            'p_value': value
        }).execute()
        
        console.print(f"[green]Secret '{name}' saved[/green]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


def get_secret(name: str = typer.Argument(..., help="Secret name to retrieve")):
    """Get a secret value."""
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    
    user_id = session['user_id']
    
    try:
        result = supabase.rpc('get_secret', {
            'p_user_id': user_id,
            'p_name': name
        }).execute()
        
        if result.data:
            console.print(f"[cyan]{name}:[/cyan] {result.data}")
        else:
            console.print(f"[yellow]Secret '{name}' not found[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


def list_secrets():
    """List all secret names (not values)."""
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    
    user_id = session['user_id']
    
    try:
        result = supabase.table("user_secrets").select("name, created_at").eq("user_id", user_id).execute()
        
        if not result.data:
            console.print("[dim]No secrets stored[/dim]")
            return
        
        table = Table(title="Your Secrets")
        table.add_column("Name", style="cyan")
        table.add_column("Created", style="dim")
        
        for secret in result.data:
            date = secret['created_at'][:10]
            table.add_row(secret['name'], date)
        
        console.print(table)
        console.print(f"\n[dim]Use 'ant secret <name>' to view value[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


def delete_secret(name: str = typer.Argument(..., help="Secret name to delete")):
    """Delete a secret."""
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    
    user_id = session['user_id']
    
    try:
        supabase.table("user_secrets").delete().eq("user_id", user_id).eq("name", name).execute()
        console.print(f"[green]Secret '{name}' deleted[/green]")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
