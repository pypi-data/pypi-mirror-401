#!/usr/bin/env python3
"""
Admin CLI - Push global tools to the backend
This stays on YOUR machine, not in the PyPI package.

Usage:
  python admin.py push fix      # Push/update the fix tool
  python admin.py list          # List all tools
  python admin.py add test      # Add a new tool interactively
"""
import requests
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

SERVER_URL = os.getenv("SERVER_URL", "http://localhost:3000")

def push_tool(slug: str):
    """Push a tool definition to the server."""
    tools_dir = Path(__file__).parent / "tool_definitions"
    tool_file = tools_dir / f"{slug}.txt"
    
    if not tool_file.exists():
        print(f"Tool definition not found: {tool_file}")
        print(f"Create it first: {tool_file}")
        return
    
    content = tool_file.read_text()
    lines = content.strip().split("\n")
    
    # Parse the file format:
    # Line 1: name
    # Line 2: description
    # Line 3: model (optional)
    # Line 4+: system prompt
    
    name = lines[0] if len(lines) > 0 else slug.title()
    description = lines[1] if len(lines) > 1 else ""
    
    # Check if line 3 is a model or prompt start
    if len(lines) > 2 and lines[2].startswith("model:"):
        model = lines[2].replace("model:", "").strip()
        system_prompt = "\n".join(lines[3:])
    else:
        model = "llama-3.1-8b-instant"
        system_prompt = "\n".join(lines[2:])
    
    payload = {
        "slug": slug,
        "name": name,
        "description": description,
        "model": model,
        "system_prompt": system_prompt,
        "active": True
    }
    
    try:
        response = requests.post(f"{SERVER_URL}/admin/tools", json=payload)
        if response.ok:
            result = response.json()
            print(f"✓ {result['status']}: {slug}")
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")


def list_tools():
    """List all tools from server."""
    try:
        response = requests.get(f"{SERVER_URL}/tools")
        if response.ok:
            tools = response.json().get("tools", [])
            print("\nGlobal Tools:")
            print("-" * 40)
            for tool in tools:
                print(f"  {tool['slug']:15} {tool['description']}")
            print()
        else:
            print(f"✗ Failed: {response.text}")
    except Exception as e:
        print(f"✗ Error: {e}")


def add_tool(slug: str):
    """Interactively create a new tool definition."""
    tools_dir = Path(__file__).parent / "tool_definitions"
    tools_dir.mkdir(exist_ok=True)
    
    tool_file = tools_dir / f"{slug}.txt"
    
    print(f"\nCreating tool: {slug}")
    print("-" * 40)
    
    name = input("Name (e.g., Fix): ").strip() or slug.title()
    description = input("Description: ").strip()
    model = input("Model [llama-3.1-8b-instant]: ").strip() or "llama-3.1-8b-instant"
    
    print("\nEnter system prompt (end with empty line):")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    system_prompt = "\n".join(lines)
    
    # Write to file
    content = f"{name}\n{description}\nmodel:{model}\n{system_prompt}"
    tool_file.write_text(content)
    
    print(f"\n✓ Saved to: {tool_file}")
    print(f"  Run: python admin.py push {slug}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        list_tools()
    elif command == "push" and len(sys.argv) > 2:
        push_tool(sys.argv[2])
    elif command == "add" and len(sys.argv) > 2:
        add_tool(sys.argv[2])
    else:
        print(__doc__)
