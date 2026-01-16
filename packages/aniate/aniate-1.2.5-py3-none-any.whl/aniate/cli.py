"""
Aniate CLI - Terminal Intelligence Layer
Clean, minimal, bundled.
"""
import sys
import typer
from rich.console import Console
from typing import Optional, List

# Core imports
from .auth import login, logout, signup, whoami, delete_account
from .commands.chat import brew_chat, delete_chat
from .commands.net import net_search
from .commands import list_intents, run_command
from .brews import save_file, fetch_file, list_files
from .brews import add_secret, get_secret, list_secrets, delete_secret
from .marketplace import publish, install, browse, unpublish

# Tool imports - bundled
from .brews.tools import fix, review, shell

console = Console()
app = typer.Typer(help="Aniate - Terminal Intelligence Layer", no_args_is_help=True)

# ============================================
# AUTH
# ============================================
app.command()(login)
app.command()(logout)
app.command(name="signup", hidden=True)(signup)  # Hidden, redirects to login
app.command()(whoami)

# ============================================
# BREW
# ============================================
app.command(name="brew.chat")(brew_chat)
app.command(name="delete.chat")(delete_chat)
app.command(name="list")(list_intents)

# ============================================
# TOOLS - Bundled, just works
# ============================================
app.command(name="fix", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(fix)
app.command(name="review", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(review)
app.command(name="shell", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(shell)
app.command(name="net", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(net_search)

# ============================================
# MARKETPLACE
# ============================================
app.command(name="publish")(publish)
app.command(name="install")(install)
app.command(name="browse")(browse)
app.command(name="unpublish")(unpublish)

# ============================================
# CLOUD
# ============================================
app.command(name="save")(save_file)
app.command(name="fetch")(fetch_file)
app.command(name="files")(list_files)

# ============================================
# SECRETS
# ============================================
app.command(name="secrets.add")(add_secret)
app.command(name="secret")(get_secret)
app.command(name="secrets")(list_secrets)
app.command(name="secrets.delete")(delete_secret)

# ============================================
# HIDDEN / DANGEROUS
# ============================================
app.command(name="run", hidden=True, context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(run_command)

# --delete is handled specially in main() since typer doesn't like -- prefixed commands

# ============================================
# HELP
# ============================================
LOGO = """
[white]                    _       _       
   __ _ _ __  (_) __ _| |_ ___
  / _` | '_ \\| |/ _` | __/ _ \\
 | (_| | | | | | (_| | ||  __/
  \\__,_|_| |_|_|\\__,_|\\__\\___|[/white]
  [red]terminal intelligence layer[/red]
"""

def help_command():
    """Show help."""
    console.print(LOGO)
    console.print("[dim]" + "─" * 50 + "[/dim]")
    
    console.print("\n[bold white]IDENTITY[/bold white]")
    console.print("  [white]login[/white]                   sign in or create account")
    console.print("  [white]logout[/white]                  end session")
    console.print("  [white]whoami[/white]                  current user")
    console.print("  [white]--delete[/white]                delete account permanently")
    
    console.print("\n[bold white]TOOLS[/bold white]")
    console.print("  [white]fix <file>[/white]              debug and fix code")
    console.print("  [white]review <file>[/white]           code review")
    console.print("  [white]shell <query>[/white]           natural language → command")
    console.print("  [white]net <query>[/white]             web intelligence")
    
    console.print("\n[bold white]BREW[/bold white]")
    console.print("  [white]brew.chat <name>[/white]        create assistant")
    console.print("  [white]delete.chat <name>[/white]      remove assistant")
    console.print("  [white]list[/white]                    show all brews")
    
    console.print("\n[bold white]MARKETPLACE[/bold white]")
    console.print("  [white]publish <name>[/white]          share your brew")
    console.print("  [white]install <user>.<name>[/white]   install from marketplace")
    
    console.print("\n[bold white]CLOUD[/bold white]")
    console.print("  [white]save <file>[/white]             upload to cloud")
    console.print("  [white]fetch <file>[/white]            download file")
    console.print("  [white]files[/white]                   list cloud files")
    
    console.print("\n[bold white]SECRETS[/bold white]")
    console.print("  [white]secrets.add <name>[/white]      store encrypted secret")
    console.print("  [white]secret <name>[/white]           retrieve secret")
    console.print("  [white]secrets[/white]                 list all secrets")
    console.print("  [white]secrets.delete <name>[/white]   remove secret")
    
    console.print("\n[bold white]CHAT[/bold white]")
    console.print("  [white]<name>[/white]                  start chat with brew")
    console.print("  [white]<name> <query>[/white]          one-shot query")
    
    console.print("\n[dim]" + "─" * 50 + "[/dim]")
    console.print("[dim]v1.2.5  •  aniate.com[/dim]\n")

app.command(name="help")(help_command)

# ============================================
# ROUTING
# ============================================
SYSTEM_COMMANDS = [
    "login", "logout", "signup", "whoami", "--delete",
    "fix", "review", "shell", "net",
    "brew.chat", "delete.chat", "list",
    "publish", "install", "browse", "unpublish",
    "save", "fetch", "files",
    "secrets.add", "secret", "secrets", "secrets.delete",
    "help", "--help"
]

def main():
    """Entry point."""
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "help":
            help_command()
            sys.exit(0)
        if cmd == "--delete":
            # Handle --delete specially
            from .auth import delete_account
            delete_account()
            sys.exit(0)
        if cmd not in SYSTEM_COMMANDS:
            sys.argv.insert(1, "run")
    app()

if __name__ == "__main__":
    main()
