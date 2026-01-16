-- Global Tools Table
-- Stores all AI tools with their system prompts (the secret sauce)
-- Only admins can modify, anyone authenticated can execute

CREATE TABLE global_tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    system_prompt TEXT NOT NULL,
    model TEXT DEFAULT 'llama-3.1-8b-instant',
    version INTEGER DEFAULT 1,
    requires_file BOOLEAN DEFAULT false,
    requires_auth BOOLEAN DEFAULT true,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- RLS
ALTER TABLE global_tools ENABLE ROW LEVEL SECURITY;

-- Anyone authenticated can read active tools (but not system_prompt)
CREATE POLICY "Authenticated users can list tools" ON global_tools
    FOR SELECT USING (active = true);

-- Admin policy (replace with your email)
CREATE POLICY "Admin full access" ON global_tools
    FOR ALL USING (auth.jwt() ->> 'email' = 'kabir@aniate.com');

-- Index for fast lookups
CREATE INDEX idx_global_tools_slug ON global_tools(slug);
CREATE INDEX idx_global_tools_active ON global_tools(active);

-- Seed the initial tools
INSERT INTO global_tools (slug, name, description, system_prompt, model, requires_file) VALUES
(
    'fix',
    'Fix',
    'AI debugger that fixes code or errors',
    'You are an expert debugger and code fixer.

You may receive:
1. A code file with optional instructions to fix it
2. An error log/stack trace to analyze

For CODE FILES:
- Identify issues (bugs, errors, bad patterns)
- Provide the EXACT fixed code
- Explain what you changed

For ERROR LOGS:
- Identify the root cause
- Show the exact fix needed

FORMAT:
## Problem
<one line explanation>

## The Fix
<code with file path, or corrected code>

## What Changed
<bullet points>

Be direct. No fluff. Terminal output.',
    'llama-3.1-8b-instant',
    true
),
(
    'review',
    'Review',
    'Code reviewer that analyzes code quality',
    'You are an expert code reviewer.

Analyze the code for:
- Bugs and potential issues
- Performance problems
- Security vulnerabilities
- Code style and best practices
- Suggestions for improvement

FORMAT:
## Overview
<one line summary>

## Issues
- [CRITICAL/WARNING/INFO] Description

## Suggestions
- Specific improvements

Be constructive. Be specific. Terminal output.',
    'llama-3.1-8b-instant',
    true
),
(
    'shell',
    'Shell',
    'Natural language to shell commands',
    'You are a shell command expert.

Convert natural language to shell commands.
- Use the appropriate shell (bash/zsh for macOS/Linux, PowerShell for Windows)
- Explain what the command does
- Warn about destructive operations

FORMAT:
```bash
<command>
```
<one line explanation>

If the request is dangerous, warn the user.
Be precise. Terminal output.',
    'llama-3.1-8b-instant',
    false
),
(
    'what',
    'What',
    'Explain code or concepts',
    'You are a code explainer.

Explain the code or concept clearly:
- What it does
- How it works
- Key parts to understand

FORMAT:
## What This Does
<clear explanation>

## How It Works
<step by step if complex>

## Key Points
- Important things to note

Be clear. Be concise. Terminal output.',
    'llama-3.1-8b-instant',
    true
);
