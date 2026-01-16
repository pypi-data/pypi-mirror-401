# Aniate Architecture V2 - Marketplace

## The Flow

```
pip install aniate          →  Gets CLI (thin client)
ant marketplace             →  Browse available tools
ant install fix             →  Downloads tool to ~/.aniate/tools/fix.json
ant fix file.py             →  Runs LOCALLY (no network call)
ant update                  →  Syncs latest tool versions
```

**Cold start once per tool. Instant execution after.**

## The Problem

Current setup bundles brews in PyPI package:
- Every new tool = new PyPI release
- System prompts are visible in package source
- No way to push global updates

## The Solution

### PyPI Package (thin client)
Only contains:
- CLI framework (Typer, Rich)
- Auth flow
- Engine (sends requests to YOUR server)
- Generic tool executor

**Rarely changes. Maybe once a month.**

### Your Backend (server.py + Supabase)
Contains:
- All system prompts (the secret sauce)
- Tool definitions (fix, review, shell, what)
- Global brews (available to all users)
- User brews (per-user assistants)
- Rate limiting, billing, analytics

**Changes frequently. Push anytime.**

---

## Database Schema

### `global_tools` table (admin-only)
```sql
CREATE TABLE global_tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT UNIQUE NOT NULL,          -- "fix", "review", "shell"
    name TEXT NOT NULL,                  -- "Fix"
    description TEXT,                    -- "AI debugger"
    system_prompt TEXT NOT NULL,         -- The secret sauce
    model TEXT DEFAULT 'llama-3.1-8b-instant',
    requires_file BOOLEAN DEFAULT false,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Only admins can modify
ALTER TABLE global_tools ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can read active tools" ON global_tools
    FOR SELECT USING (active = true);
CREATE POLICY "Admins can manage" ON global_tools
    FOR ALL USING (auth.jwt() ->> 'email' = 'kabir@aniate.com');
```

### `assistants` table (existing - user brews)
Already done. Users create their own chat brews.

---

## API Endpoints

### GET /tools
Returns all active global tools (no prompts, just metadata):
```json
[
  {"slug": "fix", "name": "Fix", "description": "AI debugger"},
  {"slug": "review", "name": "Review", "description": "Code reviewer"},
  {"slug": "shell", "name": "Shell", "description": "Natural language to shell"},
  {"slug": "what", "name": "What", "description": "Explain code"}
]
```

### POST /tool/{slug}
Execute a tool. Server fetches the system_prompt internally:
```json
{
  "content": "def foo():\n    retrun 1",
  "instructions": "fix the typo"
}
```

Response streams the AI output.

### Admin: POST /admin/tools
Push new tool or update existing:
```json
{
  "slug": "test",
  "name": "Test",
  "description": "Generate unit tests",
  "system_prompt": "You are an expert at writing unit tests..."
}
```

---

## CLI Changes

### Before (hardcoded):
```python
# brews/tools/fix.py
SYSTEM_PROMPT = """You are an expert debugger..."""  # Visible!

def fix(args):
    # Uses local SYSTEM_PROMPT
```

### After (fetched):
```python
# aniate/tools.py
def run_tool(slug: str, content: str, instructions: str = ""):
    """Generic tool executor - fetches config from server."""
    response = requests.post(
        f"{SERVER_URL}/tool/{slug}",
        headers={"Authorization": f"Bearer {token}"},
        json={"content": content, "instructions": instructions},
        stream=True
    )
    # Stream response
```

The CLI just calls `run_tool("fix", file_content, instructions)`.
Server handles the prompt, model selection, everything.

---

## Admin Workflow

When you want to add a new tool:

1. **Add to database** (via Supabase dashboard or admin CLI):
```sql
INSERT INTO global_tools (slug, name, description, system_prompt)
VALUES ('test', 'Test', 'Generate unit tests', 'You are an expert...');
```

2. **Done.** 

Users' CLI automatically sees the new tool on next run.
No PyPI release needed.

---

## What Goes Where

### PyPI Package (public, open source)
```
aniate/
├── cli.py          # Command routing
├── config.py       # URLs, keys
├── auth.py         # Login/logout
├── engine.py       # Generic LLM caller
├── tools.py        # Generic tool executor (NEW)
└── utils.py        # Helpers
```

### Your Backend (private, your server)
```
server.py           # FastAPI
├── /chat           # Chat endpoint (uses assistant config)
├── /tool/{slug}    # Tool executor (fetches prompt from DB)
├── /tools          # List available tools
├── /admin/tools    # Push new tools (admin only)
```

### Supabase (private, your database)
```
Tables:
├── users           # Auth
├── assistants      # User chat brews
├── global_tools    # Your AI tools (fix, review, etc.)
├── usage           # Analytics
└── files           # Cloud storage metadata
```

---

## Migration Steps

1. Create `global_tools` table in Supabase
2. Insert current tools (fix, review, shell, what) with their prompts
3. Add `/tool/{slug}` endpoint to server.py
4. Create thin `tools.py` in package that calls server
5. Remove `brews/tools/*.py` from package
6. Rebuild and push to PyPI (last time for this change)

From then on: Add tools via database, never touch PyPI.

---

## The Principle

> "The CLI is the interface. The server is the brain."

- CLI = dumb terminal that sends requests
- Server = smart backend that has all the prompts and logic
- Database = stores everything dynamic

This is how Cursor, v0, and every serious AI tool works.
