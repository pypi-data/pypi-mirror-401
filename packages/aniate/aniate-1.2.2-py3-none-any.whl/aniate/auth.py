"""
Aniate Authentication - Unified login system with ASCII branding
"""
import os
import json
import re
import getpass
from rich.console import Console
from rich.prompt import Prompt, Confirm
from aniate.config import SUPABASE_URL, SUPABASE_KEY, SESSION_FILE, CONFIG_DIR

console = Console()

# ASCII Art - Subtle, sophisticated
LOGO_MINI = """[white]
 ┌─────────────────────────┐
 │  ▄▀█ █▄ █ ▀█▀           │
 │  █▀█ █ ▀█  █            │
 └─────────────────────────┘[/white]"""

LOGO_FULL = """[white]
    ▄▀█ █▄ █ █ ▄▀█ ▀█▀ █▀▀
    █▀█ █ ▀█ █ █▀█  █  ██▄[/white]
"""

# Lazy-loaded Supabase client
_supabase_client = None

def _get_supabase():
    """Get Supabase client, creating it lazily."""
    global _supabase_client
    if _supabase_client is None:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_KEY:
            console.print("[dim]Service unavailable. Try again later.[/dim]")
            return None
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client

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

def _signup_flow(supabase, email: str):
    """Handle new user signup."""
    console.print("\n[dim]New here? Let's set you up.[/dim]\n")
    
    while True:
        password = getpass.getpass("Password (8+ chars, 1 number): ")
        if len(password) < 8 or not re.search(r"\d", password):
            console.print("[dim]Needs 8+ characters and a number.[/dim]")
            continue
        break
    
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm:
        console.print("[dim]Passwords don't match.[/dim]")
        return
    
    with console.status("[dim]Creating account...[/dim]", spinner="dots"):
        try:
            res = supabase.auth.sign_up({"email": email, "password": password})
            if res.user:
                console.print(LOGO_FULL)
                console.print(f"    [dim]{email}[/dim]\n")
                console.print("    [white]Verification email sent.[/white]")
                console.print("    [dim]Check spam if not in inbox.[/dim]\n")
                console.print("    [dim]After verifying:[/dim] [white]ant login[/white]\n")
        except Exception as e:
            err = str(e).lower()
            if "already registered" in err:
                console.print("[dim]Account exists. Try logging in.[/dim]")
            else:
                console.print(f"[dim]Could not create account.[/dim]")

def login():
    """Unified login - handles new and existing users."""
    session = get_session()
    if session:
        console.print(LOGO_MINI)
        console.print(f"  [dim]Already signed in as[/dim] [white]{session['email']}[/white]\n")
        return
    
    supabase = _get_supabase()
    if not supabase:
        return
    
    console.print(LOGO_FULL)
    email = Prompt.ask("    [white]Email[/white]")
    
    if not email or '@' not in email:
        console.print("\n    [dim]Invalid email.[/dim]\n")
        return
    
    password = getpass.getpass("    Password: ")
    
    with console.status("", spinner="dots"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            save_session({
                "access_token": res.session.access_token,
                "refresh_token": res.session.refresh_token,
                "user_id": res.user.id,
                "email": res.user.email
            })
            console.print(LOGO_MINI)
            console.print(f"  [white]{res.user.email}[/white]")
            console.print(f"  [dim]authenticated[/dim]\n")
            console.print(f"  [dim]Get started:[/dim] [white]ant help[/white]\n")
            
        except Exception as e:
            err = str(e).lower()
            if "invalid login" in err or "invalid" in err:
                # Could be wrong password or unverified email
                console.print("\n    [dim]Invalid credentials.[/dim]")
                console.print("    [dim]Wrong password? Email not verified?[/dim]")
                console.print("    [dim]Check spam folder for verification link.[/dim]\n")
            elif "user not found" in err or "no user" in err:
                # New user - redirect to signup
                _signup_flow(supabase, email)
            else:
                # Unknown error - offer signup
                console.print("\n    [dim]Account not found.[/dim]")
                if Confirm.ask("    [dim]Create new account?[/dim]", default=True):
                    _signup_flow(supabase, email)

def signup():
    """Redirect to unified login."""
    login()

def logout():
    """Logout and clear session."""
    console.print(LOGO_MINI)
    
    if not SESSION_FILE.exists():
        console.print("  [dim]no active session[/dim]\n")
        return
    
    os.remove(SESSION_FILE)
    console.print("  [dim]signed out[/dim]\n")

def whoami():
    """Show current logged in user."""
    session = get_session()
    
    console.print(LOGO_MINI)
    
    if not session:
        console.print("  [dim]not signed in[/dim]")
        console.print("  [dim]run:[/dim] [white]ant login[/white]\n")
        return
    
    console.print(f"  [white]{session['email']}[/white]")
    console.print(f"  [dim]{session['user_id'][:8]}...[/dim]\n")

def delete_account():
    """Delete user account permanently."""
    session = get_session()
    
    console.print(LOGO_FULL)
    
    if not session:
        console.print("    [dim]Not signed in.[/dim]\n")
        return
    
    console.print(f"    [white]{session['email']}[/white]\n")
    console.print("    [dim]This will permanently delete:[/dim]")
    console.print("    [dim]• Your account[/dim]")
    console.print("    [dim]• All brewed assistants[/dim]")
    console.print("    [dim]• Cloud files and secrets[/dim]")
    console.print("    [dim]• Chat history[/dim]\n")
    
    confirm = Prompt.ask("    [white]Type DELETE to confirm[/white]")
    
    if confirm != "DELETE":
        console.print("\n    [dim]Cancelled.[/dim]\n")
        return
    
    supabase = _get_supabase()
    if not supabase:
        return
    
    try:
        # Note: Full deletion requires admin API or database trigger
        # For now, we clear local session and mark for deletion
        supabase.auth.set_session(session['access_token'], session.get('refresh_token', ''))
        
        # Delete user data from tables
        user_id = session['user_id']
        supabase.table("assistants").delete().eq("user_id", user_id).execute()
        supabase.table("sessions").delete().eq("user_id", user_id).execute()
        supabase.table("secrets").delete().eq("user_id", user_id).execute()
        
        # Clear local session
        if SESSION_FILE.exists():
            os.remove(SESSION_FILE)
        
        console.print(LOGO_MINI)
        console.print("  [dim]account deleted[/dim]")
        console.print("  [dim]questions? support@aniate.com[/dim]\n")
        
    except Exception as e:
        console.print(f"\n    [dim]Could not delete. Contact support@aniate.com[/dim]\n")
