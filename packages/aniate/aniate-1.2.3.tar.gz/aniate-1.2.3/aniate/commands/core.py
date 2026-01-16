"""Core command utilities for assistant management and execution."""
import typer
from rich.table import Table
from supabase import create_client

from aniate.config import SUPABASE_URL, SUPABASE_KEY
from aniate.auth import get_session
from aniate.engine import run_engine
from aniate.utils import console


def list_intents():
    """List your assistants."""
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return

    # Create authenticated Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))

    res = supabase.table("assistants").select("*").eq("user_id", session['user_id']).execute()
    if not res.data:
        console.print("[dim]No assistants found.[/dim]")
        return

    table = Table(title="My Assistants")
    table.add_column("Slug", style="cyan")
    table.add_column("Role", style="white")
    table.add_column("Style", style="dim")
    
    for item in res.data:
        table.add_row(item['slug'], item['role'], f"{item['tone']}/{item['length']}")
        
    console.print(table)


def run_command(ctx: typer.Context):
    """Hidden command to run assistants."""
    args = ctx.args
    if not args:
        return
    
    slug = args[0]
    remaining_args = args[1:]
    
    session = get_session()
    if not session:
        console.print("[red]Login required. Run: ant login[/red]")
        return

    run_engine(slug, remaining_args, session)
