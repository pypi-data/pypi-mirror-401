# Aniate - Vision & Technical Documentation

> **Intelligence layer for the terminal. Brew your own AI agents.**

---

## 🎯 Vision

Aniate transforms your terminal into an intelligent workspace where you can brew custom AI agents tailored to your workflow. Instead of wrestling with complex APIs and boilerplate code, you create specialized assistants in seconds - each with unique personalities, expertise, and behaviors.

### The Problem We Solve

Traditional AI tools are:
- **Generic**: One-size-fits-all chatbots that can't adapt to specific domains
- **Disconnected**: No integration with your actual workflow and files
- **Rigid**: Can't be customized without technical expertise
- **Isolated**: Can't be shared or reused across teams

### The Aniate Solution

**Brew System Philosophy**: Create modular, reusable AI commands that:
- Integrate seamlessly with your terminal workflow
- Access your local files via `@filename` syntax
- Maintain conversation memory with cloud-synced sessions
- Can be shared through a future marketplace

---

## 🏗️ Architecture Overview

### Core Components

```
Shell/
├── config.py          # Environment & API configuration
├── auth.py            # Supabase authentication system
├── engine.py          # LLM execution engine (Groq)
├── utils.py           # File injection & prompt construction
├── main.py            # CLI entry point (Typer)
├── server.py          # FastAPI inference endpoint
├── brew.py            # Command template generator
├── commands/          # User-brewed commands
│   ├── chat.py        # Chat assistant brewing
│   ├── net.py         # Web intelligence search
│   └── core.py        # Core utilities (list, run)
└── Docs/
    ├── cheat_seet.md  # Quick reference
    └── ARCHITECTURE.md # Technical details
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **CLI** | Typer + Rich | Beautiful command-line interface |
| **LLM** | Groq API (Llama 3.1) | Fast inference engine |
| **Auth** | Supabase | User authentication & RLS |
| **Database** | PostgreSQL (Supabase) | Assistants, sessions, profiles |
| **Search** | Google Serper API | Web intelligence gathering |
| **Server** | FastAPI + Uvicorn | Local inference endpoint |

---

## 🍺 The Brew System

### What is Brewing?

**Brewing** is the act of creating a specialized AI assistant with:
- **Role**: What the assistant is (e.g., "Python Expert", "CEO of Aniate")
- **Style**: Communication approach (e.g., "Technical", "Casual")
- **Tone**: Emotional flavor (e.g., "Friendly", "Professional")
- **Formality**: Level of formality (e.g., "Formal", "Relaxed")
- **Length**: Response verbosity (e.g., "Concise", "Detailed")
- **Avoid**: Topics or behaviors to exclude

### Brew Types

#### 1. Chat Brews (`ant brew.chat`)
Custom AI assistants stored in Supabase:
```bash
ant brew.chat coder
# Creates a coding assistant accessible via:
ant coder "fix this bug @main.py"
```

#### 2. Command Brews (`ant brew.cmd`)
Custom command templates in `commands/` folder:
```bash
ant brew.cmd pdf
# Creates commands/pdf.py template
# Implement custom logic, then use:
ant pdf document.pdf
```

### Execution Modes

1. **Interactive Mode**: `ant <name>`
   - Fresh isolated chat loop
   - Full conversation history
   - Type `q` to exit

2. **One-Shot Mode**: `ant <name> message here`
   - Single query, no memory
   - Fast for quick answers
   - No quotes needed!

3. **Resume Mode**: `ant <name> <session>`
   - Load saved conversation
   - Continue where you left off
   - Auto-synced to Supabase

---

## 🔧 Key Features Built

### 1. Authentication System
- Secure signup/login via Supabase
- Session stored in `~/.aniate/session.json`
- Row-level security (RLS) policies
- Commands: `ant login`, `ant logout`, `ant whoami`

### 2. File Injection
```bash
ant coder "fix @main.py and @config.py"
```
Automatically injects file contents into prompts - no copy/paste needed.

### 3. Session Management
```bash
# In interactive mode:
> save debug-session
✔ Saved as 'debug-session'

# Resume later:
ant coder debug-session
```
Sessions auto-expire after 7 days (configurable TTL).

### 4. Token Tracking
Every API call tracks:
- `input_tokens`: Prompt size
- `output_tokens`: Response size
- `total_tokens`: Combined usage

Stored per user in database for billing/analytics.

### 5. Web Intelligence (`ant net`)
```bash
ant net latest AI developments
```
- Google Serper API search
- LLM synthesis into tactical brief
- Clean professional output
- No quotes needed!

### 6. Command Deletion
```bash
ant delete.chat coder   # Delete assistant
ant delete.cmd pdf      # Delete command template
```

---

## 🚀 What We've Accomplished

### Phase 1: Foundation ✅
- [x] Modular architecture (config, auth, engine, utils)
- [x] Supabase authentication with RLS
- [x] Groq API integration
- [x] FastAPI server for inference
- [x] Rich CLI with Typer

### Phase 2: Core Features ✅
- [x] Brew system architecture
- [x] Chat assistant creation
- [x] Command template generation
- [x] File reference injection (`@filename`)
- [x] Session save/resume system
- [x] Token usage tracking

### Phase 3: Intelligence ✅
- [x] Web search with Google Serper
- [x] Clean professional output formatting
- [x] Unquoted argument syntax
- [x] Interactive help system

### Phase 4: Polish ✅
- [x] Quit with `q` instead of `x`
- [x] List all brewed assistants
- [x] Delete commands (chat & cmd)
- [x] CEO info command
- [x] Comprehensive documentation

---

## 🔮 Future Vision

### Near-Term Roadmap

1. **Community Marketplace**
   - Share brewed commands via UUID
   - Download curated brews from others
   - Rating & review system
   - Version control for brews

2. **Enhanced Brews**
   - `ant brew.pdf` - PDF reader & analyzer
   - `ant brew.x` - X/Twitter post analyzer
   - `ant brew.code` - Code fixer & refactoring
   - `ant brew.docs` - Documentation generator

3. **Team Features**
   - Shared brews within organizations
   - Team-specific assistants
   - Collaborative sessions
   - Usage analytics dashboard

### Long-Term Vision

**Aniate becomes the standard intelligence layer for developers:**

- **Universal Integration**: Works with GitHub, Jira, Slack, etc.
- **Multi-Modal**: Image, audio, video understanding
- **Autonomous Agents**: Self-improving assistants
- **Plugin Ecosystem**: Third-party brew extensions
- **Enterprise Ready**: SSO, audit logs, compliance

---

## 💡 Key Innovations

### 1. Modular Brew Architecture
Unlike monolithic AI tools, Aniate's brew system allows:
- Infinite customization
- Easy sharing and reuse
- Version control via git
- Community contributions

### 2. Terminal-Native UX
No context switching:
```bash
ant coder "optimize @slow_function.py" > optimized.py
ant net "best practices for postgres" | tee notes.md
```

### 3. File-Aware Intelligence
The `@filename` syntax makes AI truly useful for developers:
- No copy/paste friction
- Multi-file context
- Automatic updates

### 4. Session Persistence
Cloud-synced conversations that work across:
- Multiple machines
- Team members
- Time periods

---

## 🎓 Design Principles

1. **Simplicity First**: Complex tasks should have simple interfaces
2. **Composability**: Commands should chain via Unix pipes
3. **Speed Matters**: Sub-second responses via Groq
4. **Local Control**: Your data, your machine, your rules
5. **Community Driven**: Best brews rise through marketplace

---

## 📊 Technical Metrics

- **Response Time**: ~200-500ms (Groq LLM)
- **Token Efficiency**: Prompt optimization via system prompts
- **Uptime**: 99.9% (Supabase + FastAPI)
- **Security**: RLS policies, JWT tokens, encrypted storage

---

## 🤝 Contributing

Aniate is built for the community. Future plans include:

- Open-sourcing core components
- Brew template repository
- Community marketplace
- Plugin SDK

---

## 📝 Credits

**Founded by**: Kabir Murjani (kabirmurjani@gmail.com)  
**Role**: Undergraduate Researcher | Founder, Aniate Inc.  
**Contact**: kabir.codes | @ktbir  

Built with ❤️ for developers who want intelligence at their fingertips.

---

## 🔗 Resources

- **Cheat Sheet**: [cheat_seet.md](Docs/cheat_seet.md)
- **Architecture**: [ARCHITECTURE.md](Docs/ARCHITECTURE.md)
- **GitHub**: https://github.com/Kcbir/shell

---

*Last Updated: January 14, 2026*
