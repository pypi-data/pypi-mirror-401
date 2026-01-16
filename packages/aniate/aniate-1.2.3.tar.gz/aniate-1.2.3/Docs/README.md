# Shell - Aniate CLI

> A terminal-first intelligence engine with modular architecture

## 🚀 Quick Start

```bash
# Install dependencies
pip install typer rich requests python-dotenv supabase fastapi uvicorn groq

# Start the server
uvicorn server:app --host 0.0.0.0 --port 3000

# In another terminal, use the CLI
python3 main.py login
python3 main.py create bob
python3 main.py bob "hello"
```

## 📦 Structure

```
├── __init__.py      # Package definition
├── config.py        # Constants & environment
├── utils.py         # Helpers (@file injection)
├── auth.py          # Authentication
├── engine.py        # Core execution logic
├── commands.py      # CLI interface
├── main.py          # Entry point
└── server.py        # FastAPI backend
```

## 🎯 Features

- **Smart Routing**: `ant bob "fix @main.py"` auto-routes to your assistant
- **File Injection**: `@filename` automatically injects file content
- **Session Management**: Save and resume conversations
- **Modular Design**: Each component is isolated and reusable

## 🔧 Configuration

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
GROQ_API_KEY=your_groq_api_key
SERVER_URL=http://localhost:3000
```

## 📖 Documentation

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation.

## 🛠️ Development

The modular structure makes it easy to:
- Build a VS Code extension (import `engine.py`)
- Create a web interface (reuse `auth.py` and `engine.py`)
- Test individual components
- Debug with clear stack traces

---

Built with ❤️ by Aniate
