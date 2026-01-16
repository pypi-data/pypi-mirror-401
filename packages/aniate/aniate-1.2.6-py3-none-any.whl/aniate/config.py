import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Constants
APP_NAME = "aniate"
CONFIG_DIR = Path.home() / f".{APP_NAME}"
SESSION_FILE = CONFIG_DIR / "session.json"

# API Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
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
