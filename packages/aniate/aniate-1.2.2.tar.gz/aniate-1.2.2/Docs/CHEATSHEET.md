# Aniate Quick Reference

```
                    _       _       
   __ _ _ __ (_) __ _| |_ ___
  / _` | '_ \| |/ _` | __/ _ \
 | (_| | | | | | (_| | ||  __/
  \__,_|_| |_|_|\__,_|\__\___|
                              
  Terminal Intelligence Layer
```

## Auth
```bash
ant signup              # Create account
ant login               # Authenticate
ant logout              # Clear session
ant whoami              # Current user
```

## Chat
```bash
ant <name>              # Interactive mode
ant <name> <query>      # One-shot (no quotes!)
ant <name> <session>    # Resume saved session
```

## Inside Chat
```
save <name>             # Save to cloud
@file.py                # Inject file content
q / exit                # Quit
```

## Brew Your Own
```bash
ant brew.chat <name>    # Create chat assistant
ant brew.cmd <prompt>   # AI generates command
ant brew.cmd file.py    # Load Python file
ant list                # Show all brews
ant delete.chat <name>  # Remove assistant
ant delete.cmd <name>   # Remove command
```

## Web Intelligence
```bash
ant net <query>         # Search + AI synthesis
```

## Cloud Storage
```bash
ant save <file>         # Upload to cloud
ant fetch <file>        # Download to Desktop
ant files               # List all files
```

## Secrets (Encrypted)
```bash
ant secrets.add <key>   # Store secret
ant secret <key>        # Retrieve secret
ant secrets             # List all keys
ant secrets.delete <key># Remove secret
```

## AI Tools
```bash
# Code Review
ant review file.py              # Security, perf, bugs, style

# AI Debugger (120B model)
ant fix file.py                 # Find and fix issues
ant fix file.py make it work    # Fix with instructions

# Natural Language Shell (120B model)
ant shell find large files
ant shell compress all images
ant shell delete __pycache__ folders

# Error Explainer (8B model - fast)
ant what error.log              # Explain file
ant what TypeError: ...         # Explain inline
cmd 2>&1 | ant what -           # Pipe errors
```

---

## Pro Tips

### File Injection
```bash
ant coder explain @main.py
ant coder fix @error.log
ant coder refactor @legacy.py
```

### One-Shot Without Quotes
```bash
# Just type naturally
ant coder fix the authentication bug
ant writer draft email to client about delay
```

### Chained Commands
```bash
# Create brew and use immediately
ant brew.cmd timer && ant timer 5
```

---

## Example Workflows

### Daily Standup
```bash
ant standup             # If you brewed it
```

### Code Review
```bash
ant reviewer @pull_request.diff
```

### Quick Research
```bash
ant net rust vs go performance 2025
```

### Save Important Docs
```bash
ant save ~/Documents/contract.pdf
# Access from any machine
ant fetch contract.pdf
```

---

## Directory Structure
```
~/.aniate/
├── session.json        # Auth tokens
└── custom/             # Your brews
    └── <name>.py
```

---

## Need Help?
```bash
ant --help
ant <command> --help
```

---

*Your terminal, supercharged.*
