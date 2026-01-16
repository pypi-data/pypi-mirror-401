import os
from pathlib import Path
from dotenv import load_dotenv

# App Constants
APP_NAME = "aniate"
CONFIG_DIR = Path.home() / f".{APP_NAME}"
SESSION_FILE = CONFIG_DIR / "session.json"
ENV_FILE = CONFIG_DIR / ".env"

# Load environment variables - check ~/.aniate/.env first, then current dir
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)
else:
    load_dotenv()

# API Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")  # For admin operations like delete
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:3000")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "fc97e26445cfdc9425814c9f5f45c03e41def726")

# Meta Prompt (The Soul)
META_PROMPT = """
You are Ant, a terminal-first intelligence engine built by Aniate.
You are NOT a chatbot. You are an execution layer.
Your output is rendered in a CLI. 
- Do not use markdown bolding/italics heavily and never use "*" or em dashes.
- Be extremely concise unless asked otherwise.
- If the user asks who trained you, say "I am Ant."
"""
