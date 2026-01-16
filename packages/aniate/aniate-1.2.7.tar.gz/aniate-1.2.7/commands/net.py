"""
Net Command - Web intelligence search
"""
import requests
import json
import typer
from rich.console import Console
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import SERVER_URL, SERPER_API_KEY

console = Console()

def net_search(ctx: typer.Context):
    """Search Google and synthesize intelligence briefing."""
    query_str = ' '.join(ctx.args)
    if not query_str:
        console.print("[red]Please provide a search query[/red]")
        return
    
    console.print(f"[dim]Searching: {query_str}...[/dim]")
    
    try:
        # Google Serper API
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query_str})
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers, data=payload)
        data = response.json()
        
        query = query_str  # Use joined query string for rest of function
        
        # Extract results
        results = []
        if 'organic' in data:
            for r in data['organic'][:5]:
                results.append(f"Title: {r.get('title', 'N/A')}\nLink: {r.get('link', 'N/A')}\nSnippet: {r.get('snippet', 'N/A')}\n")
        
        if not results:
            console.print("[yellow]No results found.[/yellow]")
            return
            
    except Exception as e:
        console.print(f"[red]Search failed:[/red] {e}")
        return

    # Synthesize with LLM
    raw_data = "\n---\n".join(results)
    
    system_prompt = (
        "You are an Intelligence Analyst for Aniate. "
        "Summarize search data into a tactical brief. "
        "Structure:\n"
        "1. Executive Summary (1 sentence)\n"
        "2. Key Findings (Bullets)\n"
        "3. Relevant Links\n"
        "Be concise and professional."
    )
    
    user_message = f"Search data for '{query}':\n\n{raw_data}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
    
    try:
        with console.status("Synthesizing...", spinner="dots"):
            res = requests.post(SERVER_URL, json={"messages": messages}).json()["output"]
            
        console.print(f"\n[bold cyan]Query:[/bold cyan] {query}")
        console.print("[dim]" + "─" * 80 + "[/dim]")
        console.print(res)
        console.print("[dim]" + "─" * 80 + "[/dim]\n")
        
    except Exception as e:
        console.print(f"[red]Analysis failed:[/red] {e}")
