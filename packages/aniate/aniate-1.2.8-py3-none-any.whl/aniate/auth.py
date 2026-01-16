"""
Aniate Authentication - Beautiful, minimal, with username support
"""
import os
import json
import re
import getpass
from rich.console import Console
from rich.prompt import Prompt, Confirm
from aniate.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY, SESSION_FILE, CONFIG_DIR

console = Console()

# Classic Aniate ASCII - Red accent
LOGO = """
[white]                    _       _       
   __ _ _ __  (_) __ _| |_ ___
  / _` | '_ \\| |/ _` | __/ _ \\
 | (_| | | | | | (_| | ||  __/
  \\__,_|_| |_|_|\\__,_|\\__\\___|[/white]
"""

# Lazy-loaded Supabase client
_supabase_client = None

def _get_supabase():
    """Get Supabase client, creating it lazily."""
    global _supabase_client
    if _supabase_client is None:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_KEY:
            console.print("[dim]Service unavailable.[/dim]")
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

def _check_username_available(supabase, username: str) -> bool:
    """Check if username is available."""
    try:
        result = supabase.table("profiles").select("username").eq("username", username).execute()
        return len(result.data) == 0
    except:
        return True  # Assume available if check fails

def _signup_flow(supabase, email: str):
    """Handle new user signup with username."""
    console.print("\n[dim]Creating account...[/dim]\n")
    
    # Username
    while True:
        username = Prompt.ask("[white]Username[/white]").strip().lower()
        if not username:
            console.print("[dim]Username required.[/dim]")
            continue
        if len(username) < 3:
            console.print("[dim]At least 3 characters.[/dim]")
            continue
        if not re.match(r'^[a-z0-9_]+$', username):
            console.print("[dim]Letters, numbers, underscore only.[/dim]")
            continue
        if not _check_username_available(supabase, username):
            console.print("[dim]Already taken. Try another.[/dim]")
            continue
        break
    
    # Password
    while True:
        password = getpass.getpass("Password (8+ chars, 1 number): ")
        if len(password) < 8 or not re.search(r"\d", password):
            console.print("[dim]Needs 8+ characters and a number.[/dim]")
            continue
        break
    
    confirm = getpass.getpass("Confirm: ")
    if password != confirm:
        console.print("[dim]Passwords don't match.[/dim]")
        return
    
    with console.status("[dim]...[/dim]", spinner="dots"):
        try:
            # Sign up with username in metadata
            res = supabase.auth.sign_up({
                "email": email, 
                "password": password,
                "options": {
                    "data": {"username": username}
                }
            })
            if res.user:
                # Create profile with username
                try:
                    supabase.table("profiles").insert({
                        "id": res.user.id,
                        "username": username,
                        "email": email
                    }).execute()
                except:
                    pass  # Profile might be created by trigger
                
                console.print()
                console.print(f"  [red]@{username}[/red]")
                console.print(f"  [dim]{email}[/dim]\n")
                console.print("  [white]Check email to verify.[/white]")
                console.print("  [dim]Then:[/dim] ant login\n")
        except Exception as e:
            err = str(e).lower()
            if "already registered" in err:
                console.print("[dim]Account exists. Try logging in.[/dim]")
            else:
                console.print("[dim]Could not create account.[/dim]")

def login():
    """Unified login - handles new and existing users."""
    session = get_session()
    if session:
        console.print(LOGO)
        username = session.get('username', '')
        if username:
            console.print(f"  [red]@{username}[/red]")
        console.print(f"  [dim]{session['email']}[/dim]")
        console.print("  [dim]already signed in[/dim]\n")
        return
    
    supabase = _get_supabase()
    if not supabase:
        return
    
    console.print(LOGO)
    console.print("  [red]ANIATE[/red] [dim]login[/dim]\n")
    email = Prompt.ask("  [white]email[/white]")
    
    if not email or '@' not in email:
        console.print("  [dim]invalid email[/dim]\n")
        return
    
    password = getpass.getpass("  password: ")
    
    with console.status("[dim]...[/dim]", spinner="dots"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
            
            # Get username from profile
            username = None
            try:
                profile = supabase.table("profiles").select("username").eq("id", res.user.id).execute()
                if profile.data:
                    username = profile.data[0].get('username')
            except:
                pass
            
            save_session({
                "access_token": res.session.access_token,
                "refresh_token": res.session.refresh_token,
                "user_id": res.user.id,
                "email": res.user.email,
                "username": username
            })
            
            console.print()
            if username:
                console.print(f"  [red]@{username}[/red]")
            console.print(f"  [dim]{res.user.email}[/dim]")
            console.print("  [white]authenticated[/white]\n")
            
        except Exception as e:
            err = str(e).lower()
            console.print()  # End spinner output
    
    # Handle errors OUTSIDE the spinner context
    if 'err' in dir():
        if "invalid" in err:
            console.print("  [dim]invalid credentials or account not found[/dim]")
            if Confirm.ask("  [dim]create new account?[/dim]", default=True):
                _signup_flow(supabase, email)
            else:
                console.print("  [dim]check spam for verification link if you signed up[/dim]\n")
        elif err:
            console.print(f"  [dim]error: {err[:50]}[/dim]")
            if Confirm.ask("  [dim]create account?[/dim]", default=True):
                _signup_flow(supabase, email)

def signup():
    """Redirect to unified login."""
    login()

def logout():
    """Logout and clear session."""
    console.print(LOGO)
    
    if not SESSION_FILE.exists():
        console.print("  [dim]no active session[/dim]\n")
        return
    
    os.remove(SESSION_FILE)
    console.print("  [dim]signed out[/dim]\n")

def whoami():
    """Show current logged in user."""
    session = get_session()
    
    console.print(LOGO)
    
    if not session:
        console.print("  [dim]not signed in[/dim]")
        console.print("  [dim]run:[/dim] ant login\n")
        return
    
    username = session.get('username', '')
    if username:
        console.print(f"  [red]@{username}[/red]")
    console.print(f"  [dim]{session['email']}[/dim]")
    console.print(f"  [dim]{session['user_id'][:8]}...[/dim]\n")

def delete_account():
    """Delete user account permanently."""
    session = get_session()
    
    console.print(LOGO)
    console.print("  [red]DELETE ACCOUNT[/red]\n")
    
    if not session:
        console.print("  [dim]not signed in[/dim]\n")
        return
    
    username = session.get('username', '')
    if username:
        console.print(f"  [red]@{username}[/red]")
    console.print(f"  [dim]{session['email']}[/dim]\n")
    
    console.print("  [white]⚠  WARNING[/white]")
    console.print("  [dim]this permanently deletes:[/dim]")
    console.print("  [dim]• your account[/dim]")
    console.print("  [dim]• all brews[/dim]")
    console.print("  [dim]• all files[/dim]")
    console.print("  [dim]• all secrets[/dim]")
    console.print("  [dim]• marketplace listings[/dim]\n")
    console.print("  [red]THIS CANNOT BE UNDONE[/red]\n")
    
    # Verify password
    password = getpass.getpass("  confirm password: ")
    if not password:
        console.print("\n  [dim]cancelled[/dim]\n")
        return
    
    supabase = _get_supabase()
    if not supabase:
        return
    
    # Verify password is correct by signing in
    try:
        supabase.auth.sign_in_with_password({"email": session['email'], "password": password})
    except:
        console.print("\n  [dim]incorrect password[/dim]\n")
        return
    
    confirm = Prompt.ask("  [white]type DELETE to confirm[/white]")
    
    if confirm != "DELETE":
        console.print("\n  [dim]cancelled[/dim]\n")
        return
    
    user_id = session['user_id']
    
    with console.status("[dim]deleting...[/dim]", spinner="dots"):
        # Use service key for admin-level deletion (deletes from auth.users which cascades)
        if SUPABASE_SERVICE_KEY and SUPABASE_URL:
            try:
                from supabase import create_client
                admin_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
                # Delete from auth.users - this cascades to profiles and all FK tables
                admin_client.auth.admin.delete_user(user_id)
                
                # Clear local session
                if SESSION_FILE.exists():
                    os.remove(SESSION_FILE)
                
                console.print()
                console.print("  [green]✓[/green] [dim]account deleted[/dim]")
                console.print("  [dim]for help: support@aniate.com[/dim]\n")
                return
            except Exception as e:
                pass  # Fall through to manual cleanup
        
        # Fallback: Delete from tables manually if service key not available
        tables_to_clean = ["assistants", "sessions", "user_secrets", "user_files", "marketplace"]
        for table in tables_to_clean:
            try:
                supabase.table(table).delete().eq("user_id", user_id).execute()
            except:
                pass
        
        try:
            supabase.table("profiles").delete().eq("id", user_id).execute()
        except:
            pass
    
    # Clear local session
    if SESSION_FILE.exists():
        os.remove(SESSION_FILE)
    
    console.print()
    console.print("  [dim]local session cleared[/dim]")
    console.print("  [yellow]note: auth account requires manual deletion[/yellow]")
    console.print("  [dim]go to supabase dashboard > auth > users[/dim]")
    console.print("  [dim]for help: support@aniate.com[/dim]\n")
