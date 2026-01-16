import os
import json
import re
import getpass
from rich.console import Console
from rich.prompt import Prompt
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, SESSION_FILE, CONFIG_DIR

console = Console()
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_session():
    """Load session from file."""
    if not SESSION_FILE.exists():
        return None
    try:
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    except:
        return None

def save_session(data):
    """Save session to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(SESSION_FILE, 'w') as f:
        json.dump(data, f)

def signup():
    """Create a new account."""
    session = get_session()
    if session:
        console.print("[yellow]Already logged in. Run: ant logout[/yellow]")
        return
    
    console.print("\n[bold white]ANIATE[/bold white] [dim]Create Account[/dim]\n")
    email = Prompt.ask("[white]Email[/white]")
    while True:
        password = getpass.getpass("Password (8+ chars, 1 number): ")
        if len(password) < 8 or not re.search(r"\d", password):
            console.print("[red]Password too weak. Try again.[/red]")
            continue
        break
    with console.status("[dim]Creating account...[/dim]", spinner="dots"):
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            if res.user:
                console.print(f"\n[green]Account created.[/green] {email}")
                console.print("[dim]Check your email to verify.\n[/dim]")
            else:
                console.print("[yellow]Account created. Check email for verification.[/yellow]")
        except Exception as e:
            console.print(f"[red]Failed:[/red] {str(e)}")

def login():
    """Login via Email/Password."""
    session = get_session()
    if session:
        console.print(f"[dim]Already authenticated as[/dim] {session['email']}")
        return
    
    console.print("\n[bold white]ANIATE[/bold white] [dim]Login[/dim]\n")
    email = Prompt.ask("[white]Email[/white]")
    password = getpass.getpass("Password: ")
    
    with console.status("[dim]Authenticating...[/dim]", spinner="dots"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            save_session({
                "access_token": res.session.access_token,
                "refresh_token": res.session.refresh_token,
                "user_id": res.user.id,
                "email": res.user.email
            })
            console.print(f"\n[green]Authenticated.[/green] {res.user.email}\n")
        except Exception as e:
            console.print(f"[red]Authentication failed.[/red] Check credentials.")

def logout():
    """Logout and clear session."""
    if not SESSION_FILE.exists():
        console.print("[dim]No active session.[/dim]")
        return
    
    os.remove(SESSION_FILE)
    console.print("[dim]Session cleared.[/dim]")

def whoami():
    """Show current logged in user."""
    session = get_session()
    if not session:
        console.print("[dim]No active session. Run: ant login[/dim]")
        return
    
    console.print(f"\n[white]{session['email']}[/white]")
    console.print(f"[dim]{session['user_id']}[/dim]\n")
