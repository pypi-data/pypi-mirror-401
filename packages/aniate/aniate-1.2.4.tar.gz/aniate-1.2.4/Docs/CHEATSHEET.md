# Aniate Quick Reference

```
                    _       _       
   __ _ _ __  (_) __ _| |_ ___
  / _` | '_ \| |/ _` | __/ _ \
 | (_| | | | | | (_| | ||  __/
  \__,_|_| |_|_|\__,_|\__\___|
                              
  terminal intelligence layer
```

## Identity
```bash
ant login               # Sign in or create account
ant logout              # End session
ant whoami              # Current user
```

## AI Tools
```bash
ant fix file.py              # Debug and fix code
ant fix file.py make it work # Fix with instructions

ant review file.py           # Security, perf, bugs, style

ant shell find large files   # Natural language → command
ant shell compress images    # Just describe what you want

ant net latest AI news       # Web intelligence search
```

## Brew Your Own
```bash
ant brew.chat <name>    # Create chat assistant
ant list                # Show all brews
ant delete.chat <name>  # Remove assistant
```

## Marketplace
```bash
ant publish <name>           # Share your brew publicly
ant install kabir.helper     # Install someone's brew
ant browse                   # See popular brews
ant unpublish <name>         # Remove from marketplace
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
q                       # Quit
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

---

## Pro Tips

### File Injection
```bash
ant coder explain @main.py
ant coder fix @error.log
```

### One-Shot Without Quotes
```bash
ant coder fix the authentication bug
ant writer draft email to client
```

### Share Your Best Brews
```bash
ant brew.chat helper         # Create
ant publish helper           # Share
# Others can: ant install yourname.helper
```

---

## Example Workflows

### Code Review
```bash
ant review pull_request.diff
```

### Quick Research
```bash
ant net rust vs go 2025
```

### Team Brew
```bash
# Create a team assistant
ant brew.chat standup
ant publish standup
# Team members: ant install team.standup
```

---

## Directory Structure
```
~/.aniate/
├── session.json        # Auth tokens
└── history.json        # Command history
```

---

*Your terminal, supercharged.*
