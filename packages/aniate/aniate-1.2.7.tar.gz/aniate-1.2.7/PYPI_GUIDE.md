# PyPI Publishing Guide

## The Architecture

```
PyPI Package (aniate/)     →  Thin client, rarely changes
Your Server (server.py)    →  All the logic, prompts, brains
Supabase (global_tools)    →  Tool definitions stored here
```

**Adding new tools does NOT require a PyPI release.**

---

## Quick Upload (when you change the CLI)

```bash
# Build
python3 -m build

# Upload to PyPI
python3 -m twine upload dist/*
```

When prompted:
- **Username**: `__token__`
- **Password**: Your PyPI API token (starts with `pypi-`)

## Using API Token

Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Then just run:
```bash
python3 -m twine upload dist/*
```

## Version Bumps

When you add new features:

1. Update version in `pyproject.toml`:
```toml
version = "1.0.1"
```

2. Update version in `aniate/__init__.py`:
```python
__version__ = "1.0.1"
```

3. Clean old builds:
```bash
rm -rf dist/ build/ *.egg-info
```

4. Build and upload:
```bash
python3 -m build
python3 -m twine upload dist/*
```

## What Gets Uploaded?

The `aniate/` directory containing:
```
aniate/
├── __init__.py
├── cli.py          # Main entry point (was main.py)
├── config.py
├── auth.py
├── engine.py
├── utils.py
├── brew.py
├── commands/
├── brews/
├── custom/
└── game/
```

## What Stays Local (Not Uploaded)?

```
server.py           # Backend - deploy separately
.env                # Secrets
migrations/         # Database
SQL/                # Database schemas
Docs/               # Internal documentation
```

## After Upload

Users can install with:
```bash
pip install aniate
```

And use immediately:
```bash
ant help
ant login
ant brew.chat coder
```

## Test on TestPyPI First (Optional)

```bash
# Upload to test server
python3 -m twine upload --repository testpypi dist/*

# Install from test server
pip install -i https://test.pypi.org/simple/ aniate
```

---

## Workflow Summary

Every time you add a feature:

1. Make changes in `aniate/` directory
2. Bump version number
3. `rm -rf dist/ && python3 -m build`
4. `python3 -m twine upload dist/*`

That's it. Users get it with `pip install --upgrade aniate`.

---

## Adding New Tools (No PyPI Release Needed)

### Method 1: Via Admin CLI
```bash
# Create a new tool definition
python admin.py add test

# Push to server
python admin.py push test

# List all tools
python admin.py list
```

### Method 2: Direct Database Insert
```sql
INSERT INTO global_tools (slug, name, description, system_prompt)
VALUES ('test', 'Test', 'Generate unit tests', 'You are an expert...');
```

### Method 3: Via API
```bash
curl -X POST http://your-server.com/admin/tools \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "test",
    "name": "Test",
    "description": "Generate unit tests",
    "system_prompt": "You are an expert..."
  }'
```

Users immediately get the new tool. No pip install needed.

---

## When to Release PyPI

Only release when you change:
- CLI commands (new built-in command)
- Auth flow
- Core engine logic
- Dependencies

**NOT** for:
- New tools (stored in DB)
- Updated prompts (stored in DB)
- New chat brews (stored in DB)
