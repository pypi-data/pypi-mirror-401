import re
from pathlib import Path
from rich.console import Console

console = Console()

def resolve_file_references(text):
    """Injects @filename content into the prompt."""
    matches = re.findall(r"@([\w\-\./]+)", text)
    for filename in matches:
        path = Path(filename)
        if path.exists() and path.is_file():
            try:
                content = path.read_text()
                injection = f"\n<file name='{filename}'>\n{content}\n</file>\n"
                text = text.replace(f"@{filename}", injection)
                console.print(f"[dim]✔ Injected {filename}[/dim]")
            except Exception as e:
                console.print(f"[yellow]⚠ Could not read @{filename}[/yellow]")
    return text

def construct_system_prompt(assistant):
    """Stitches the 6 DB columns into one Master Prompt."""
    prompt = f"{assistant['role']}.\n"
    prompt += f"Speaking Style: {assistant['speaking_style']}.\n"
    prompt += f"Tone: {assistant['tone']}.\n"
    prompt += f"Formality: {assistant['formality']}.\n"
    prompt += f"Length Constraint: {assistant['length']}.\n"
    
    if assistant['things_to_avoid']:
        prompt += f"STRICTLY AVOID: {assistant['things_to_avoid']}.\n"
        
    return prompt
