# Aniate Architecture - PyPI & Open Source Strategy

## Overview

This document outlines the strategic architecture for:
1. **PyPI Distribution** (`pip install aniate`)
2. **Backend Infrastructure** (what stays on your servers)
3. **Open Source Strategy** (what to share, what to protect)

---

## The Golden Rule

> **Open source the CLIENT. Monetize the INFRASTRUCTURE.**

This is how every successful dev tool does it:
- **Terraform**: CLI open source, Terraform Cloud is paid
- **Supabase**: Client libraries open source, hosted platform paid
- **Vercel**: Next.js open source, hosting paid
- **Docker**: Docker Engine open source, Docker Hub paid

---

## Architecture Split

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           OPEN SOURCE (PyPI)                            │
│                         pip install aniate                              │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   main.py   │  │  config.py  │  │   auth.py   │  │  engine.py  │   │
│  │    CLI      │  │   Config    │  │  Auth Flow  │  │  LLM Core   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────────────┐ │
│  │  utils.py   │  │ commands/   │  │           brews/                │ │
│  │  Helpers    │  │  Core Cmds  │  │   tools/, secrets/, storage/    │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ HTTPS API Calls
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        PRIVATE BACKEND (Your Servers)                   │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                         API Gateway                                │ │
│  │                    api.aniate.com / ant.api                        │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                    │                                    │
│         ┌──────────────────────────┼──────────────────────────┐        │
│         ▼                          ▼                          ▼        │
│  ┌─────────────┐           ┌─────────────┐           ┌─────────────┐  │
│  │   Auth      │           │  Inference  │           │   Billing   │  │
│  │  Service    │           │   Service   │           │   Service   │  │
│  │             │           │             │           │             │  │
│  │ - JWT       │           │ - Groq API  │           │ - Stripe    │  │
│  │ - Sessions  │           │ - Rate Limit│           │ - Usage     │  │
│  │ - RLS       │           │ - Queue     │           │ - Tiers     │  │
│  └─────────────┘           └─────────────┘           └─────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                          Supabase                                  │ │
│  │   PostgreSQL + Storage + RLS + RPC Functions + Realtime           │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                     SECRET SAUCE (Never Open Source)               │ │
│  │                                                                    │ │
│  │  - Meta Prompt engineering (the "soul" of Ant)                    │ │
│  │  - Rate limiting algorithms                                        │ │
│  │  - Billing/usage tracking logic                                    │ │
│  │  - Premium brew implementations                                    │ │
│  │  - Model routing logic (which model for what)                     │ │
│  │  - Caching strategies                                              │ │
│  │  - Analytics/telemetry                                             │ │
│  └───────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## File-by-File Breakdown

### OPEN SOURCE (PyPI Package)

```
aniate/
├── __init__.py           # Package init
├── __main__.py           # Entry point: python -m aniate
├── cli.py                # Main Typer app (current main.py)
├── config.py             # API URLs, app constants (NO SECRETS)
├── auth.py               # Login/logout/signup/whoami
├── engine.py             # LLM execution, interactive loop
├── utils.py              # File helpers, prompt building
│
├── commands/
│   ├── __init__.py
│   ├── core.py           # list, run, help
│   ├── chat.py           # brew.chat, delete.chat
│   └── net.py            # Web search
│
├── brews/
│   ├── __init__.py
│   ├── maker.py          # brew.cmd AI generator
│   │
│   ├── tools/            # Built-in AI tools
│   │   ├── __init__.py
│   │   ├── fix.py        # ant fix
│   │   ├── review.py     # ant review
│   │   ├── shell.py      # ant shell
│   │   └── what.py       # ant what
│   │
│   ├── storage/          # Cloud storage
│   │   ├── __init__.py
│   │   ├── save.py
│   │   ├── fetch.py
│   │   └── files.py
│   │
│   └── secrets/          # Secrets management
│       ├── __init__.py
│       └── secrets.py
│
└── py.typed              # Type hints marker
```

### PRIVATE BACKEND (Your Servers)

```
aniate-backend/
├── api/
│   ├── main.py                 # FastAPI app
│   ├── routes/
│   │   ├── inference.py        # /v1/chat endpoint
│   │   ├── auth.py             # /v1/auth/* endpoints
│   │   └── billing.py          # /v1/billing/* endpoints
│   │
│   ├── services/
│   │   ├── groq_client.py      # Groq API wrapper
│   │   ├── model_router.py     # Which model for what task
│   │   ├── rate_limiter.py     # Per-user rate limiting
│   │   ├── usage_tracker.py    # Token counting, billing
│   │   └── cache.py            # Response caching
│   │
│   ├── prompts/                # THE SECRET SAUCE
│   │   ├── meta_prompt.py      # Ant's personality
│   │   ├── fix_prompt.py       # ant fix system prompt
│   │   ├── review_prompt.py    # ant review system prompt
│   │   └── shell_prompt.py     # ant shell system prompt
│   │
│   └── middleware/
│       ├── auth.py             # JWT validation
│       ├── logging.py          # Request logging
│       └── cors.py             # CORS config
│
├── workers/
│   ├── billing_worker.py       # Process usage -> Stripe
│   └── analytics_worker.py     # Aggregate analytics
│
├── migrations/                  # Supabase migrations
│   ├── 001_profiles.sql
│   ├── 002_assistants.sql
│   └── ...
│
└── infra/
    ├── docker-compose.yml
    ├── Dockerfile
    └── fly.toml / railway.json
```

---

## What Goes Where

### PyPI Package (Open Source)

| File | Purpose | Why Open Source? |
|------|---------|------------------|
| `cli.py` | Command routing | Users need to run it |
| `auth.py` | Login/logout | Standard auth flow |
| `engine.py` | Chat execution | Core functionality |
| `brews/tools/*` | fix, review, shell, what | Community can contribute |
| `brews/storage/*` | save, fetch, files | Standard CRUD |
| `brews/secrets/*` | secrets management | Standard CRUD |

**Key Change**: The open source version calls YOUR API, not Groq directly.

```python
# config.py (open source version)
API_BASE = "https://api.aniate.com/v1"

# engine.py (open source version)
def call_llm(messages, model="default"):
    response = requests.post(
        f"{API_BASE}/chat",
        headers={"Authorization": f"Bearer {session['access_token']}"},
        json={"messages": messages, "model": model}
    )
    return response.json()
```

### Backend (Private)

| Component | Purpose | Why Private? |
|-----------|---------|--------------|
| Meta prompts | Ant's personality | Your IP |
| Model routing | GPT-4 vs 8B vs 120B | Business logic |
| Rate limiting | Usage controls | Monetization |
| Billing logic | Stripe integration | Revenue |
| Caching | Performance | Competitive edge |
| Analytics | User insights | Business intelligence |

---

## Strategic Open Source Layers

### Layer 1: Fully Open (Community Growth)
```
OK  CLI framework
OK  Auth flow
OK  Basic brews (tools/)
OK  Custom brew structure
OK  Documentation
```

### Layer 2: Open but Calls Your API (Lock-in)
```
OK  LLM calls -> api.aniate.com
OK  Storage -> Supabase (your instance)
OK  Secrets -> Your encrypted storage
```

### Layer 3: Never Open (Monetization)
```
NO  Meta prompts (the "soul")
NO  Rate limiting logic
NO  Billing/usage tracking
NO  Premium brews
NO  Model selection logic
NO  Caching strategies
```

---

## PyPI Package Structure

### pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "aniate"
version = "1.0.0"
description = "Terminal-first AI intelligence layer"
readme = "README.md"
license = "MIT"
authors = [
    { name = "Kabir Murjani", email = "kabirmurjani@gmail.com" }
]
keywords = ["ai", "cli", "terminal", "llm", "assistant"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Topic :: Software Development :: Libraries :: Python Modules",
]
requires-python = ">=3.10"
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "requests>=2.28.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
]

[project.scripts]
ant = "aniate.cli:app"

[project.urls]
Homepage = "https://aniate.com"
Documentation = "https://docs.aniate.com"
Repository = "https://github.com/aniateai/aniateai"
```

### Installation Experience

```bash
# User installs
pip install aniate

# First run
ant login
# Opens browser -> aniate.com/auth -> redirects back with token

# Start using
ant brew.chat coder
ant coder help me debug this

# Upgrade to Pro
ant upgrade  # Opens billing page
```

---

## Self-Hosted Option (Enterprise)

For enterprise customers who want to run everything themselves:

```bash
# They pay for a license, get access to:
docker pull aniate/server:enterprise

# Includes:
# - Full backend code
# - All prompts
# - Self-contained (bring your own Groq key)
```

---

## Revenue Protection

### What stops someone from forking?

1. **API dependency**: Open source client calls YOUR API
2. **No prompts**: The "magic" is in your backend prompts
3. **No billing logic**: They can't monetize without building it
4. **Supabase lock-in**: Data is on YOUR Supabase instance
5. **Rate limiting**: Free tier is limited, Pro is generous
6. **Model access**: You control which models users get

### If someone forks and self-hosts:

- They need their own Groq API key ($$)
- They need to write their own prompts (hard)
- They need their own backend (work)
- They lose cloud sync, sessions, billing
- They're now maintaining infrastructure

**Net result**: Power users might fork. 99% will just pay $19/mo.

---

## Migration Plan

### Phase 1: Refactor Current Code
```
1. Move server.py logic to backend repo
2. Update client to call API_BASE instead of SERVER_URL
3. Remove hardcoded Groq API key from client
4. Add proper error handling for API failures
```

### Phase 2: Package for PyPI
```
1. Restructure into proper Python package
2. Add pyproject.toml
3. Test installation: pip install -e .
4. Publish to PyPI test: twine upload --repository testpypi
5. Verify: pip install -i https://test.pypi.org/simple/ aniate
```

### Phase 3: Deploy Backend
```
1. Deploy FastAPI backend to Fly.io / Railway
2. Set up api.aniate.com subdomain
3. Configure rate limiting
4. Set up Stripe billing
5. Monitor and scale
```

### Phase 4: Launch
```
1. Publish to PyPI: pip install aniate
2. Announce on Twitter, HN, Reddit
3. Monitor usage, iterate
```

---

## Files to NEVER Open Source

```
XX  prompts/meta_prompt.py      # Ant's soul
XX  prompts/*_prompt.py         # All system prompts
XX  services/model_router.py    # Model selection logic
XX  services/rate_limiter.py    # Rate limiting
XX  services/usage_tracker.py   # Billing logic
XX  services/cache.py           # Caching strategy
XX  workers/billing_worker.py   # Stripe integration
XX  .env                        # API keys
XX  migrations/                 # DB schema (gives away structure)
```

---

## Current Code Changes Needed

### Move to Backend (Private)

| Current File | New Location | Reason |
|--------------|--------------|--------|
| `server.py` | `backend/api/main.py` | Controls inference |
| `META_PROMPT` in config.py | `backend/prompts/meta.py` | Secret sauce |
| System prompts in tools | `backend/prompts/*.py` | Secret sauce |

### Stays in Client (Open Source)

| Current File | Status | Notes |
|--------------|--------|-------|
| `main.py` | Keep | Rename to `cli.py` |
| `auth.py` | Keep | Calls your auth API |
| `engine.py` | Modify | Call API instead of local server |
| `utils.py` | Keep | Helper functions |
| `commands/*` | Keep | Command implementations |
| `brews/*` | Keep | But system prompts move to backend |

---

## Summary Table

| Component | PyPI (Open) | Backend (Private) |
|-----------|-------------|-------------------|
| CLI routing | ✅ | |
| Auth flow | ✅ | |
| Chat execution | ✅ | |
| Tool brews (fix, review, etc) | ✅ (logic only) | ✅ (prompts) |
| Cloud storage | ✅ | ✅ (Supabase) |
| LLM inference | | ✅ |
| Meta prompts | | ✅ |
| Rate limiting | | ✅ |
| Billing | | ✅ |
| Model routing | | ✅ |

---

**The Strategy**: Give away the car, sell the gas.

---

*Built by Kabir Murjani | kabir.codes | @ktbir*
