import requests
from rich.console import Console
from rich.prompt import Prompt
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, SERVER_URL
from utils import resolve_file_references, construct_system_prompt

console = Console()

def increment_chat_count(user_session, prompt_tokens=0, completion_tokens=0):
    """Increment the user's chat count and token usage in Supabase."""
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        supabase.auth.set_session(user_session['access_token'], user_session.get('refresh_token', ''))
        supabase.rpc('increment_user_chat_count', {
            'user_id': user_session['user_id'], 
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens
        }).execute()
    except:
        pass  # Silently fail if count update fails

def run_engine(slug, remaining_args, user_session):
    """The Brain: Handles one-shot, interactive, and session resume."""
    # Create authenticated Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    supabase.auth.set_session(user_session['access_token'], user_session.get('refresh_token', ''))
    
    # Fetch Assistant Data
    res = supabase.table("assistants").select("*").eq("slug", slug).eq("user_id", user_session['user_id']).execute()
    if not res.data:
        console.print(f"[red]Ant '{slug}' not found.[/red]")
        return
    assistant = res.data[0]
    
    # Build System Prompt
    system_prompt_text = construct_system_prompt(assistant)
    messages = []
    session_id = None
    
    # CASE A: Resume Session (ant kabir session_name)
    if len(remaining_args) == 1 and not remaining_args[0].startswith("-") and " " not in remaining_args[0]:
        possible_name = remaining_args[0]
        sess_res = supabase.table("sessions").select("*").eq("assistant_id", assistant['id']).eq("session_name", possible_name).execute()
        
        if sess_res.data:
            console.print(f"[dim]Resuming '{possible_name}'[/dim]")
            messages = sess_res.data[0]['messages']
            session_id = sess_res.data[0]['id']
            interactive_loop(assistant, system_prompt_text, messages, session_id, possible_name, user_session, supabase)
            return

    # CASE B: One-Shot (ant kabir "fix @main.py")
    if remaining_args:
        raw_input = " ".join(remaining_args)
        final_input = resolve_file_references(raw_input)
        
        msgs = [
            {"role": "system", "content": system_prompt_text},
            {"role": "user", "content": final_input}
        ]
        try:
            response = requests.post(SERVER_URL, json={"messages": msgs}).json()
            out = response["output"]
            console.print(out)
            usage = response.get("usage", {})
            increment_chat_count(user_session, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
        return

    # CASE C: New Interactive (ant kabir)
    messages = [{"role": "system", "content": system_prompt_text}]
    interactive_loop(assistant, system_prompt_text, messages, None, None, user_session, supabase)

def interactive_loop(assistant, sys_prompt, messages, session_id, session_name, user_session, supabase):
    """Interactive chat loop with save capability."""
    console.print(f"[bold green]{assistant['slug']}[/bold green] (type 'exit' to quit, 'save <name>' to save)")
    
    # Replay existing messages
    for m in messages:
        if m['role'] == 'user':
            console.print(f"[cyan]You:[/cyan] {m['content']}")
        if m['role'] == 'assistant':
            console.print(f"[green]Ant:[/green] {m['content']}")

    while True:
        user_input = Prompt.ask("[cyan]>[/cyan]")
        
        if user_input.lower() in ['exit', 'q', 'quit']:
            break
        
        # Save Command
        if user_input.startswith("save "):
            new_name = user_input.split(" ", 1)[1]
            data = {
                "user_id": user_session['user_id'],
                "assistant_id": assistant['id'],
                "session_name": new_name,
                "messages": messages
            }
            if session_id:
                supabase.table("sessions").update(data).eq("id", session_id).execute()
            else:
                try:
                    res = supabase.table("sessions").insert(data).execute()
                    session_id = res.data[0]['id']
                except:
                    supabase.table("sessions").update(data).eq("assistant_id", assistant['id']).eq("session_name", new_name).execute()
            console.print(f"[bold green]✔ Saved as '{new_name}'[/bold green]")
            continue

        # Process user input
        final_input = resolve_file_references(user_input)
        messages.append({"role": "user", "content": final_input})
        
        try:
            with console.status("", spinner="dots"):
                response = requests.post(SERVER_URL, json={"messages": messages}).json()
                res = response["output"]
            console.print(f"[green]{res}[/green]")
            messages.append({"role": "assistant", "content": res})
            usage = response.get("usage", {})
            increment_chat_count(user_session, usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0))
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
