import sys
import typer
from rich.console import Console
from commands.chat import brew_chat, delete_chat
from commands.net import net_search
from brew import delete_cmd
from auth import login, logout, signup, whoami
from brews import save_file, fetch_file, list_files
from brews import add_secret, get_secret, list_secrets, delete_secret
from brews import brew_make

# Tool brews
from brews.tools import fix, review, shell, what

# Custom brews
from game.guess import guess
from custom.timer import timer

# Import list_intents and run_command from old commands.py
from commands import list_intents, run_command

console = Console()
app = typer.Typer(help="Aniate CLI - Brew your intelligence layer", no_args_is_help=True)

# Auth commands
app.command()(login)
app.command()(logout)
app.command()(signup)
app.command()(whoami)

# Brew commands
app.command(name="brew.chat")(brew_chat)
app.command(name="brew.cmd", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(brew_make)
app.command(name="delete.chat")(delete_chat)
app.command(name="delete.cmd")(delete_cmd)

# Core commands
app.command(name="net", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(net_search)
app.command(name="save")(save_file)
app.command(name="fetch")(fetch_file)
app.command(name="files")(list_files)
app.command(name="list")(list_intents)

# Secrets management
app.command(name="secrets.add")(add_secret)
app.command(name="secret")(get_secret)
app.command(name="secrets")(list_secrets)
app.command(name="secrets.delete")(delete_secret)

# AI Brew Maker
app.command(name="brew.make", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(brew_make)

# Custom brews
app.command(name="guess")(guess)
app.command(name="timer")(timer)

# Tool brews (AI-powered)
app.command(name="fix", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(fix)
app.command(name="review", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(review)
app.command(name="shell", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(shell)
app.command(name="what", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(what)

app.command(name="run", hidden=True, context_settings={"allow_extra_args": True, "ignore_unknown_options": True})(run_command)

LOGO = """
[white]                    _       _       
   __ _ _ __  (_) __ _| |_ ___
  / _` | '_ \\| |/ _` | __/ _ \\
 | (_| | | | | | (_| | ||  __/
  \\__,_|_| |_|_|\\__,_|\\__\\___|[/white]
                              
  [red]Terminal Intelligence Layer[/red]
"""

def help_command():
    """Show comprehensive help information."""
    console.print(LOGO)
    console.print("[dim]" + "-" * 50 + "[/dim]")
    
    console.print("\n[bold white]IDENTITY[/bold white]")
    console.print("  [white]signup[/white]                  Create account")
    console.print("  [white]login[/white]                   Authenticate")
    console.print("  [white]logout[/white]                  Clear session")
    console.print("  [white]whoami[/white]                  Current user")
    
    console.print("\n[bold white]BREW[/bold white]")
    console.print("  [white]brew.chat <name>[/white]        Create chat assistant")
    console.print("  [white]brew.cmd <prompt>[/white]       Generate command with AI")
    console.print("  [white]delete.chat <name>[/white]      Remove assistant")
    console.print("  [white]delete.cmd <name>[/white]       Remove command")
    console.print("  [white]list[/white]                    Show all brews")
    
    console.print("\n[bold white]TOOLS[/bold white]")
    console.print("  [white]fix <file>[/white]              Debug and fix code")
    console.print("  [white]review <file>[/white]           Code review")
    console.print("  [white]shell <query>[/white]           Natural language to shell")
    console.print("  [white]what <error>[/white]            Explain errors")
    console.print("  [white]net <query>[/white]             Web intelligence")
    
    console.print("\n[bold white]CLOUD[/bold white]")
    console.print("  [white]save <file>[/white]             Upload to cloud")
    console.print("  [white]fetch <file>[/white]            Download to Desktop")
    console.print("  [white]files[/white]                   List cloud files")
    
    console.print("\n[bold white]SECRETS[/bold white]")
    console.print("  [white]secrets.add <name>[/white]      Store encrypted secret")
    console.print("  [white]secret <name>[/white]           Retrieve secret")
    console.print("  [white]secrets[/white]                 List all secrets")
    console.print("  [white]secrets.delete <name>[/white]   Remove secret")
    
    console.print("\n[bold white]EXECUTION[/bold white]")
    console.print("  [white]<name>[/white]                  Interactive mode")
    console.print("  [white]<name> <query>[/white]          One-shot execution")
    console.print("  [white]<name> <session>[/white]        Resume saved session")
    
    console.print("\n[dim]" + "-" * 50 + "[/dim]")
    console.print("[dim]v1.0.0  |  aniate.com  |  Ant[/dim]\n")

def ceo_command():
    """Display information about the founder."""
    console.print("\n[bold cyan]Kabir Murjani[/bold cyan]")
    console.print("[white]Undergraduate Researcher | Founder, Aniate Inc.[/white]\n")
    console.print("[bold]CORRESPONDENCE[/bold]")
    console.print("-" * 80)
    console.print("[cyan]EMAIL:[/cyan]      kabirmurjani@gmail.com")
    console.print("[cyan]WEB:[/cyan]        kabir.codes")
    console.print("[cyan]X:[/cyan]          @ktbir\n")

app.command(name="help")(help_command)
app.command(name="--ceo", hidden=True)(ceo_command)

if __name__ == "__main__":
    # Router Logic: Intercept non-system commands and route to 'run'
    SYSTEM_COMMANDS = ["brew.chat", "brew.cmd", "delete.chat", "delete.cmd", "list", "login", "logout", "signup", "whoami", "net", "save", "fetch", "files", "secrets", "secrets.add", "secret", "secrets.delete", "guess", "timer", "fix", "review", "shell", "what", "help", "--help", "--ceo"]
    
    # Convert 'help' to show custom help
    if len(sys.argv) > 1 and sys.argv[1] == "help":
        help_command()
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] == "--ceo":
        ceo_command()
        sys.exit(0)
    elif len(sys.argv) > 1 and sys.argv[1] not in SYSTEM_COMMANDS:
        sys.argv.insert(1, "run")
    
    app()
