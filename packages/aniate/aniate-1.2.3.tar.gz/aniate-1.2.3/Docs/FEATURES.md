# Aniate - Complete Feature Documentation & Roadmap

> **Terminal-first intelligence layer. Your AI, your rules.**

---

## Current Features (v1.0)

### Authentication & Identity
| Command | Description |
|---------|-------------|
| `ant signup` | Create account with email/password |
| `ant login` | Authenticate and save session locally |
| `ant logout` | Clear local credentials |
| `ant whoami` | Display current logged-in user |

**Technical:** Sessions stored in `~/.aniate/session.json`, Supabase JWT auth with refresh tokens.

---

### Brew System - Custom AI Assistants

#### Create Assistants
| Command | Description |
|---------|-------------|
| `ant brew.chat <name>` | Interactive wizard to create chat assistant |
| `ant brew.cmd <prompt>` | AI generates command code using GPT-OSS-120B |
| `ant brew.cmd file.py` | Load existing Python file as brew |
| `ant list` | Show all your brewed assistants |
| `ant delete.chat <name>` | Remove assistant |
| `ant delete.cmd <name>` | Remove command |

#### Assistant Properties
- **Role**: What the AI is (e.g., "Senior Python Developer")
- **Style**: Communication approach (e.g., "Technical", "Casual")
- **Tone**: Emotional flavor (e.g., "Friendly", "Direct")
- **Formality**: Level (e.g., "Formal", "Relaxed")
- **Length**: Response verbosity (e.g., "Concise", "Detailed")
- **Avoid**: Topics/behaviors to exclude

---

### Chat Execution Modes

```bash
# Interactive Mode - Full conversation with memory
ant coder

# One-Shot Mode - Single query, no memory (no quotes needed!)
ant coder fix the bug in main.py

# Resume Mode - Continue saved conversation
ant coder debug-session
```

#### Inside Interactive Mode
| Command | Description |
|---------|-------------|
| `save <name>` | Save conversation to cloud (7-day TTL) |
| `@filename` | Inject file content into prompt |
| `q` or `exit` | Quit session |

---

### Web Intelligence

```bash
ant net latest AI developments
ant net what happened in tech today
```

**Features:**
- Google Serper API for real-time search
- LLM synthesis into tactical briefing
- Clean professional output
- No quotes needed

---

### Cloud Storage

```bash
# Upload from anywhere
ant save report.pdf
ant save ~/Documents/notes.txt

# Download to Desktop
ant fetch report.pdf

# List all files
ant files
```

**Features:**
- Supabase Storage (S3-compatible)
- Per-user isolation via RLS
- Sync across any terminal/machine

---

### Secrets Management

```bash
# Store encrypted API key
ant secrets.add openai_key
# Enter value: (hidden input)

# Retrieve
ant secret openai_key

# List all (names only)
ant secrets

# Delete
ant secrets.delete openai_key
```

**Security:**
- PGP encryption (pgcrypto)
- Server-side decrypt only
- RLS isolation
- Even DB admins see only encrypted values

---

### Token Tracking

Every API call tracks:
- `input_tokens` - Prompt size
- `output_tokens` - Response size
- `total_tokens` - Combined

Stored per-user for billing/analytics.

---

### AI Tools (Built-in Brews)

#### Code Review
```bash
ant review config.py           # Review any file
ant review src/auth.py         # Security, performance, bugs, style
```

#### AI Debugger  
```bash
ant fix main.py                # Find and fix issues
ant fix buggy.py make it work  # Fix with specific instructions
ant fix error.log              # Analyze error log
```

#### Natural Language Shell
```bash
ant shell find large files
ant shell show disk usage
ant shell compress images in current folder
ant shell delete all __pycache__ folders
ant shell show git history for main.py
```

#### Error Explainer
```bash
ant what error.log                    # Explain errors in a file
ant what TypeError: cannot read       # Explain inline error
python script.py 2>&1 | ant what -    # Pipe errors directly
```

**Models Used:**
- `ant fix`, `ant review`, `ant shell` → GPT-OSS-120B (reasoning)
- `ant what` → llama-3.1-8b-instant (fast)

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     TERMINAL (CLI)                       │
│                        main.py                           │
└─────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   auth.py     │  │  engine.py    │  │   brews/      │
│   Login/Auth  │  │   LLM Core    │  │  Extensions   │
└───────────────┘  └───────────────┘  └───────────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
┌─────────────────────────────────────────────────────────┐
│                    server.py (FastAPI)                   │
│                    Groq LLM Inference                    │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                      SUPABASE                            │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌──────────┐  │
│  │profiles │  │assistants│  │sessions │  │user_files│  │
│  └─────────┘  └──────────┘  └─────────┘  └──────────┘  │
│                    + Storage Bucket                      │
└─────────────────────────────────────────────────────────┘
```

---

## "Shut Up and Take My Money" Brew Ideas

### 1. `ant commit` - AI Git Commits
```bash
ant commit
# Analyzes staged changes
# Generates semantic commit message
# Optionally pushes
```
**Why it's killer:** Never write a commit message again. AI understands diff context.

---

### 2. `ant review @pr.diff` - Code Review
```bash
ant review @changes.diff
# Or pipe directly:
git diff | ant review
```
**Output:** Security issues, performance concerns, style violations, suggestions.

---

### 3. `ant fix @error.log` - Auto Debug
```bash
ant fix @error.log
# Reads error, finds file, suggests fix
# Optional: --apply to auto-fix
```
**Why it's killer:** Stack trace → solution in seconds.

---

### 4. `ant docs @src/` - Auto Documentation
```bash
ant docs @module.py
# Generates docstrings, README, API docs
```
**Output:** Markdown documentation, type hints, examples.

---

### 5. `ant sql "find users who signed up last week"` - Natural Language SQL
```bash
ant sql "show me top 10 customers by revenue"
# Connects to your DB (credentials in ant secrets)
# Generates and optionally runs query
```
**Why it's killer:** Non-technical people can query databases.

---

### 6. `ant shell "find large files"` - Natural Language Shell
```bash
ant shell "delete all node_modules folders"
ant shell "compress images in this folder"
```
**Output:** Shows command, asks confirmation, executes.

---

### 7. `ant watch @server.log` - Real-time Log Analysis
```bash
ant watch @/var/log/nginx/error.log
# Monitors log file
# Alerts on anomalies
# Suggests fixes for errors
```
**Why it's killer:** 24/7 AI watching your logs.

---

### 8. `ant api "create user endpoint"` - API Generator
```bash
ant api "CRUD for products with auth"
# Generates FastAPI/Express routes
# Includes validation, error handling
```

---

### 9. `ant test @function.py` - Auto Test Generation
```bash
ant test @utils.py
# Generates pytest/jest tests
# Edge cases, mocks, fixtures
```

---

### 10. `ant refactor @legacy.py` - Code Modernization
```bash
ant refactor @old_code.py --style=clean
# Modernizes syntax
# Improves performance
# Adds type hints
```

---

### 11. `ant explain @complex.py` - Code Explainer
```bash
ant explain @algorithm.py
# Line-by-line explanation
# Complexity analysis
# Visual diagrams (ASCII)
```

---

### 12. `ant secure @app/` - Security Audit
```bash
ant secure @src/
# Scans for vulnerabilities
# OWASP top 10 checks
# Dependency audit
```

---

### 13. `ant mock "stripe payment API"` - Mock API Generator
```bash
ant mock "github oauth flow"
# Generates mock server
# Realistic responses
# Error scenarios
```

---

### 14. `ant translate @app/ --to=spanish` - i18n Automation
```bash
ant translate @components/ --to=french,german,japanese
# Extracts strings
# AI translation with context
# Generates locale files
```

---

### 15. `ant diagram @architecture.md` - ASCII Diagrams
```bash
ant diagram "microservices with kafka"
# Generates ASCII art diagrams
# System architecture visualization
```

---

### 16. `ant email "follow up on proposal"` - Email Drafting
```bash
ant email "thank client for meeting, schedule follow up"
# Uses your writing style (learned from ant secrets)
# Copy to clipboard
```

---

### 17. `ant standup` - Daily Standup Generator
```bash
ant standup
# Reads git commits from yesterday
# Checks calendar
# Generates standup update
```

---

### 18. `ant invoice client_name 5000` - Invoice Generator
```bash
ant invoice "Acme Corp" 5000 --hours=20
# Generates PDF invoice
# Stores in cloud (ant files)
# Tracks in database
```

---

### 19. `ant pitch "AI code review tool"` - Pitch Deck Generator
```bash
ant pitch "marketplace for developers"
# Generates slide content
# Problem/Solution/Market/Team structure
# Export to Markdown or PDF
```

---

### 20. `ant scrape "https://example.com"` - Smart Web Scraper
```bash
ant scrape "https://news.ycombinator.com" --extract="titles,links"
# AI-powered content extraction
# Handles dynamic content
# Respects robots.txt
```

---

## Premium Features (Future SaaS)

### Team Collaboration
- Shared brews within organization
- Team-specific assistants
- Usage analytics dashboard
- Admin controls

### Brew Marketplace
- Publish your brews
- Discover community brews
- Rating & reviews
- Revenue sharing for creators

### Enterprise
- SSO integration
- Audit logs
- Compliance (SOC2, HIPAA)
- On-premise deployment
- Custom LLM endpoints

### Advanced Models
- GPT-4 / Claude integration
- Custom fine-tuned models
- Multi-modal (images, audio)
- Long context windows

---

## Monetization Strategy

### Free Tier
- 100 queries/month
- 3 custom assistants
- 100MB cloud storage
- Community brews

### Pro ($19/month)
- Unlimited queries
- Unlimited assistants
- 10GB cloud storage
- Priority inference
- Advanced models (GPT-4)

### Team ($49/user/month)
- Everything in Pro
- Shared brews
- Team management
- Analytics dashboard
- Priority support

### Enterprise (Custom)
- On-premise option
- SSO/SAML
- Audit logs
- Dedicated support
- Custom integrations

---

## Technical Roadmap

### Q1 2026
- [ ] `ant commit` - AI git commits
- [ ] `ant review` - Code review
- [ ] `ant fix` - Auto debug
- [ ] Brew marketplace MVP

### Q2 2026
- [ ] `ant sql` - Natural language SQL
- [ ] `ant shell` - Natural language shell
- [ ] Team collaboration
- [ ] Usage analytics

### Q3 2026
- [ ] `ant watch` - Log monitoring
- [ ] `ant secure` - Security audit
- [ ] Enterprise features
- [ ] Mobile app (SSH wrapper)

### Q4 2026
- [ ] Multi-modal support
- [ ] Custom model training
- [ ] Plugin SDK
- [ ] API for third-party integrations

---

## Why Aniate Wins

| Traditional AI Tools | Aniate |
|---------------------|--------|
| Browser-based | Terminal-native |
| Generic responses | Custom-trained assistants |
| No file access | `@filename` injection |
| No persistence | Cloud-synced sessions |
| One-size-fits-all | Brew your own commands |
| Vendor lock-in | Open architecture |

---

## The Vision

**Aniate becomes the intelligence layer between developers and their tools.**

Every terminal command enhanced with AI. Every workflow automated. Every developer 10x more productive.

Not a chatbot. An execution layer.

---

*Built by Kabir Murjani | kabir.codes | @ktbir*
