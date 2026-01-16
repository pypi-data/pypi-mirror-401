"""
Chat Command - Brew conversational assistants
"""
import requests
from rich.console import Console
from rich.prompt import Prompt
from supabase import create_client
import sys
import os
# Package imports

from aniate.config import SUPABASE_URL, SUPABASE_KEY
from aniate.auth import get_session

console = Console()

def brew_chat(name: str):
    """Brew a new chat assistant with custom traits."""
    session = get_session()
    if not session:
        console.print("[dim]Authentication required. Run: ant login[/dim]")
        return

    # Create authenticated Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))

    # Check for duplicates
    existing = supabase.table("assistants").select("*").eq("slug", name).eq("user_id", session['user_id']).execute()
    if existing.data:
        console.print(f"[dim]'{name}' already exists.[/dim]")
        return

    console.print(f"\n[bold white]BREW[/bold white] [dim]{name}[/dim]")
    console.print("[dim]All fields optional. Enter to skip.[/dim]\n")
    
    # Meta Prompt - the most important one
    console.print("[white]Meta Prompt[/white] [dim]Core instruction for AI behavior[/dim]")
    console.print("[dim]e.g. You are a ruthless startup advisor who gives brutally honest feedback[/dim]")
    role = Prompt.ask("[dim]>[/dim]", default="").strip()
    
    console.print()
    
    # Style traits - all optional with hints
    console.print("[white]Traits[/white] [dim]Optional[/dim]\n")
    
    style = Prompt.ask("[dim]Style (Technical, Casual, Academic)[/dim]", default="").strip()
    tone = Prompt.ask("[dim]Tone (Direct, Friendly, Witty)[/dim]", default="").strip()
    formality = Prompt.ask("[dim]Formality (Formal, Relaxed)[/dim]", default="").strip()
    length = Prompt.ask("[dim]Length (Concise, Detailed)[/dim]", default="").strip()
    avoid = Prompt.ask("[dim]Avoid (No emojis, No code)[/dim]", default="").strip()

    try:
        # Build insert data - role defaults to "Assistant" for vanilla mode
        insert_data = {
            "user_id": session['user_id'],
            "slug": name,
            "role": role if role else "Assistant",  # Default for DB constraint
            "speaking_style": style if style else None,
            "tone": tone if tone else None,
            "formality": formality if formality else None,
            "length": length if length else None,
            "things_to_avoid": avoid if avoid else None
        }
        
        supabase.table("assistants").insert(insert_data).execute()
        
        if role or style or tone or formality or length or avoid:
            console.print(f"\n[green]Created.[/green] {name}")
        else:
            console.print(f"\n[green]Created.[/green] {name} [dim](vanilla)[/dim]")
        console.print(f"[dim]Run: ant {name}[/dim]\n")
    except Exception as e:
        console.print(f"[red]Failed:[/red] {e}")

def delete_chat(name: str):
    """Delete a brewed chat assistant."""
    session = get_session()
    if not session:
        console.print("[dim]Authentication required. Run: ant login[/dim]")
        return

    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))

    existing = supabase.table("assistants").select("*").eq("slug", name).eq("user_id", session['user_id']).execute()
    if not existing.data:
        console.print(f"[dim]'{name}' not found.[/dim]")
        return

    try:
        supabase.table("assistants").delete().eq("slug", name).eq("user_id", session['user_id']).execute()
        console.print(f"[dim]Deleted.[/dim] {name}")
    except Exception as e:
        console.print(f"[red]Failed:[/red] {e}")
