"""
Marketplace - Share and install brews from other users
ant publish <name>        - Share your brew
ant install <user>.<name> - Install someone's brew
"""
from rich.console import Console
from rich.table import Table
from rich.prompt import Confirm
from supabase import create_client
from aniate.config import SUPABASE_URL, SUPABASE_KEY
from aniate.auth import get_session

console = Console()

LOGO = """
[white]                    _       _       
   __ _ _ __  (_) __ _| |_ ___
  / _` | '_ \\| |/ _` | __/ _ \\
 | (_| | | | | | (_| | ||  __/
  \\__,_|_| |_|_|\\__,_|\\__\\___|[/white]
"""

def _get_supabase():
    """Get authenticated Supabase client."""
    session = get_session()
    if not session:
        return None, None
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
    return supabase, session

def publish(name: str):
    """Publish a brew to the marketplace."""
    supabase, session = _get_supabase()
    if not supabase:
        console.print("[dim]Login required. Run: ant login[/dim]")
        return
    
    # Get the assistant
    result = supabase.table("assistants").select("*").eq("slug", name).eq("user_id", session['user_id']).execute()
    
    if not result.data:
        console.print(f"[dim]Brew '{name}' not found.[/dim]")
        return
    
    assistant = result.data[0]
    username = session.get('username')
    
    if not username:
        console.print("[dim]Username required to publish.[/dim]")
        console.print("[dim]Update your profile with a username.[/dim]")
        return
    
    # Check if already published
    existing = supabase.table("marketplace").select("id").eq("user_id", session['user_id']).eq("slug", name).execute()
    
    if existing.data:
        # Update existing
        supabase.table("marketplace").update({
            "role": assistant.get('role'),
            "speaking_style": assistant.get('speaking_style'),
            "tone": assistant.get('tone'),
            "formality": assistant.get('formality'),
            "length": assistant.get('length'),
            "things_to_avoid": assistant.get('things_to_avoid'),
        }).eq("id", existing.data[0]['id']).execute()
        
        console.print(LOGO)
        console.print(f"  [white]@{username}.{name}[/white]")
        console.print("  [dim]updated in marketplace[/dim]\n")
    else:
        # Create new listing
        supabase.table("marketplace").insert({
            "user_id": session['user_id'],
            "username": username,
            "slug": name,
            "role": assistant.get('role'),
            "speaking_style": assistant.get('speaking_style'),
            "tone": assistant.get('tone'),
            "formality": assistant.get('formality'),
            "length": assistant.get('length'),
            "things_to_avoid": assistant.get('things_to_avoid'),
            "installs": 0
        }).execute()
        
        console.print(LOGO)
        console.print(f"  [red]@{username}.{name}[/red]")
        console.print("  [dim]published to marketplace[/dim]")
        console.print(f"  [dim]others can install:[/dim] ant install {username}.{name}\n")

def install(identifier: str):
    """Install a brew from marketplace. Format: username.brewname"""
    if '.' not in identifier:
        console.print("[dim]Format: ant install username.brewname[/dim]")
        return
    
    parts = identifier.split('.', 1)
    if len(parts) != 2:
        console.print("[dim]Format: ant install username.brewname[/dim]")
        return
    
    target_username, brew_name = parts
    
    supabase, session = _get_supabase()
    if not supabase:
        console.print("[dim]Login required. Run: ant login[/dim]")
        return
    
    # Find the brew in marketplace
    result = supabase.table("marketplace").select("*").eq("username", target_username).eq("slug", brew_name).execute()
    
    if not result.data:
        console.print(f"[dim]'{identifier}' not found in marketplace.[/dim]")
        return
    
    brew = result.data[0]
    
    # Check if user already has a brew with this name
    existing = supabase.table("assistants").select("id").eq("slug", brew_name).eq("user_id", session['user_id']).execute()
    
    if existing.data:
        console.print(f"[dim]You already have a brew named '{brew_name}'.[/dim]")
        if not Confirm.ask("[dim]Overwrite?[/dim]", default=False):
            return
        supabase.table("assistants").delete().eq("id", existing.data[0]['id']).execute()
    
    # Install the brew
    supabase.table("assistants").insert({
        "user_id": session['user_id'],
        "slug": brew_name,
        "role": brew.get('role'),
        "speaking_style": brew.get('speaking_style'),
        "tone": brew.get('tone'),
        "formality": brew.get('formality'),
        "length": brew.get('length'),
        "things_to_avoid": brew.get('things_to_avoid'),
        "source": f"@{target_username}"  # Track origin
    }).execute()
    
    # Increment install count
    supabase.table("marketplace").update({
        "installs": brew.get('installs', 0) + 1
    }).eq("id", brew['id']).execute()
    
    console.print(LOGO)
    console.print(f"  [white]{brew_name}[/white] [dim]from[/dim] [red]@{target_username}[/red]")
    console.print("  [dim]installed[/dim]")
    console.print(f"  [dim]run:[/dim] ant {brew_name}\n")

def browse():
    """Browse popular brews in marketplace."""
    supabase, session = _get_supabase()
    if not supabase:
        console.print("[dim]Login required. Run: ant login[/dim]")
        return
    
    # Get top brews by installs
    result = supabase.table("marketplace").select("*").order("installs", desc=True).limit(20).execute()
    
    if not result.data:
        console.print(LOGO)
        console.print("  [dim]No brews in marketplace yet.[/dim]")
        console.print("  [dim]Be the first:[/dim] ant publish <name>\n")
        return
    
    console.print(LOGO)
    
    table = Table(show_header=True, header_style="bold white", box=None)
    table.add_column("Brew", style="white")
    table.add_column("By", style="red")
    table.add_column("Role", style="dim")
    table.add_column("Installs", style="dim", justify="right")
    
    for brew in result.data:
        table.add_row(
            brew['slug'],
            f"@{brew['username']}",
            (brew.get('role') or 'Assistant')[:30],
            str(brew.get('installs', 0))
        )
    
    console.print(table)
    console.print("\n[dim]Install:[/dim] ant install username.brewname\n")

def unpublish(name: str):
    """Remove a brew from marketplace."""
    supabase, session = _get_supabase()
    if not supabase:
        console.print("[dim]Login required. Run: ant login[/dim]")
        return
    
    result = supabase.table("marketplace").delete().eq("slug", name).eq("user_id", session['user_id']).execute()
    
    console.print(LOGO)
    if result.data:
        console.print(f"  [dim]{name} removed from marketplace[/dim]\n")
    else:
        console.print(f"  [dim]{name} not found in your published brews[/dim]\n")
