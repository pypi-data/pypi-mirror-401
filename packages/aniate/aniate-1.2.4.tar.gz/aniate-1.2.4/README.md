# Aniate

> Terminal-first AI intelligence layer.

```
                    _       _       
   __ _ _ __  (_) __ _| |_ ___
  / _` | '_ \| |/ _` | __/ _ \
 | (_| | | | | | (_| | ||  __/
  \__,_|_| |_|_|\__,_|\__\___|
                              
  Terminal Intelligence Layer
```

## Installation

```bash
pip install aniate
```

## Quick Start

```bash
# Create account
ant signup

# Login
ant login

# Create your first AI assistant
ant brew.chat coder

# Use it
ant coder help me debug this function
```

## Features

### Brew Custom AI Assistants

```bash
ant brew.chat writer      # Create a writing assistant
ant brew.cmd "security scanner"  # AI generates the code
```

### AI-Powered Tools

```bash
ant fix main.py           # Debug and fix code
ant review config.py      # Code review
ant shell find large files # Natural language to shell
ant what error.log        # Explain errors
```

### Cloud Sync

```bash
ant save report.pdf       # Upload to cloud
ant fetch report.pdf      # Download anywhere
ant files                 # List cloud files
```

### Encrypted Secrets

```bash
ant secrets.add openai_key  # Store encrypted
ant secret openai_key       # Retrieve
```

## Commands

| Command | Description |
|---------|-------------|
| `ant signup` | Create account |
| `ant login` | Authenticate |
| `ant logout` | Clear session |
| `ant whoami` | Current user |
| `ant brew.chat <name>` | Create chat assistant |
| `ant brew.cmd <prompt>` | AI generates command |
| `ant list` | Show all brews |
| `ant fix <file>` | Debug and fix code |
| `ant review <file>` | Code review |
| `ant shell <query>` | NL to shell |
| `ant what <error>` | Explain errors |
| `ant net <query>` | Web intelligence |
| `ant save <file>` | Upload to cloud |
| `ant fetch <file>` | Download |
| `ant files` | List cloud files |
| `ant help` | Show all commands |

## Execution Modes

```bash
# Interactive mode
ant coder

# One-shot (no quotes needed)
ant coder fix the authentication bug

# Resume saved session
ant coder my-debug-session
```

## Inside Chat

```
save <name>    # Save conversation to cloud
@filename      # Inject file content
exit           # Quit
```

## Links

- Website: [aniate.com](https://aniate.com)
- Documentation: [docs.aniate.com](https://docs.aniate.com)
- Twitter: [@ktbir](https://twitter.com/aniateai)

## License

MIT License - Kabir Murjani
