# Aniate CLI - Brew System Cheat Sheet

## System & Identity
- `ant signup` - Create new Aniate account (8+ char password)
- `ant login` - Login via email/password (Session saved to ~/.aniate/session.json)
- `ant logout` - Clear local credentials
- `ant whoami` - Show current logged-in user

## 🍺 Brew System
- `ant brew.chat <name>` - Brew a new chat assistant (Interactive wizard)
- `ant brew.cmd <name>` - Brew a custom command template
- `ant delete.chat <name>` - Delete a chat assistant
- `ant delete.cmd <name>` - Delete a custom command
- `ant list` - Show all your brewed chats

## Core Commands
- `ant net query` - Search web & synthesize intelligence briefing

## Chat Execution
- `ant <name>` - Interactive Mode (Fresh isolated chat loop)
- `ant <name> message` - One-Shot Mode (Runs once, no memory)
- `ant <name> <session>` - Resume Mode (Loads history from Supabase)

## Inside Chat (Interactive Mode)
- `save <name>` - Save conversation to cloud (7-day TTL)
- `@filename` - Inject file content (e.g., `@main.py`)
- `exit` / `q` - Quit chat

## Utilities
- `ant help` - Show help
- `ant --ceo` - Founder info

---

💡 **Brew Philosophy**: Create modular, reusable commands. Future marketplace-ready.

ant net query here
ant net latest AI developments
ant net what is today's date