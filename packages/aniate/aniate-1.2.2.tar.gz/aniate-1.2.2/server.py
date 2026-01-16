import os
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import StreamingResponse
from groq import Groq
from supabase import create_client
from typing import Optional
import uvicorn
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
# uvicorn server:app --host 0.0.0.0 --port 3000

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

# THE META PROMPT (The "Soul" of Ant)
META_PROMPT = """You are Ant, a terminal-first intelligence engine built by Aniate."""

@app.post("/")
async def chat(req: Request):
    body = await req.json()
    messages = body.get("messages")
    
    if not messages:
        raise HTTPException(status_code=400, detail="Missing messages")
    
    # INJECT THE SOUL
    # We prepend the Meta Prompt to the very start of the conversation
    if messages and messages[0]["role"] == "system":
        messages[0]["content"] = META_PROMPT + "\n\n" + messages[0]["content"]
    else:
        messages.insert(0, {"role": "system", "content": META_PROMPT})

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        max_completion_tokens=1028,
        temperature=0.7,
        top_p=0.8,
    )

    return {
        "output": completion.choices[0].message.content,
        "usage": {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens
        }
    }

"""
curl -X POST http://localhost:3000 \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      { "role": "system", "content": "You are a student." },
      { "role": "user", "content": "how are ya" }
    ]
  }'
"""

# ============================================
# TOOLS API - Dynamic tool execution
# ============================================

@app.get("/tools")
async def list_tools():
    """List all available global tools (without system prompts)."""
    result = supabase.table("global_tools").select(
        "slug, name, description, requires_file"
    ).eq("active", True).execute()
    return {"tools": result.data}


@app.get("/marketplace")
async def marketplace():
    """Public marketplace - list tools for browsing (no prompts)."""
    result = supabase.table("global_tools").select(
        "slug, name, description, version"
    ).eq("active", True).execute()
    return {"tools": result.data}


@app.get("/tool/{slug}/download")
async def download_tool(slug: str, authorization: Optional[str] = Header(None)):
    """Download a tool config for local installation. Includes system_prompt."""
    
    # In production: verify auth token here
    
    tool = supabase.table("global_tools").select(
        "slug, name, description, system_prompt, model, version"
    ).eq("slug", slug).eq("active", True).single().execute()
    
    if not tool.data:
        raise HTTPException(status_code=404, detail=f"Tool '{slug}' not found")
    
    return tool.data


@app.post("/tool/{slug}")
async def execute_tool(slug: str, req: Request, authorization: Optional[str] = Header(None)):
    """Execute a global tool by slug (for users without local install)."""
    
    # Get the tool config from database (includes secret system_prompt)
    tool = supabase.table("global_tools").select("*").eq("slug", slug).eq("active", True).single().execute()
    
    if not tool.data:
        raise HTTPException(status_code=404, detail=f"Tool '{slug}' not found")
    
    body = await req.json()
    content = body.get("content", "")
    instructions = body.get("instructions", "")
    
    # Build the message
    user_message = content
    if instructions:
        user_message = f"{content}\n\nInstructions: {instructions}"
    
    messages = [
        {"role": "system", "content": tool.data["system_prompt"]},
        {"role": "user", "content": user_message}
    ]
    
    completion = client.chat.completions.create(
        model=tool.data.get("model", "llama-3.1-8b-instant"),
        messages=messages,
        max_completion_tokens=2048,
        temperature=0.7,
    )
    
    return {
        "output": completion.choices[0].message.content,
        "tool": slug,
        "usage": {
            "prompt_tokens": completion.usage.prompt_tokens,
            "completion_tokens": completion.usage.completion_tokens,
            "total_tokens": completion.usage.total_tokens
        }
    }


# ============================================
# ADMIN API - Manage tools (protected)
# ============================================

ADMIN_EMAILS = ["kabir@aniate.com"]  # Add your admin emails

@app.post("/admin/tools")
async def upsert_tool(req: Request, authorization: Optional[str] = Header(None)):
    """Create or update a global tool. Admin only."""
    
    # Verify admin (you'd validate the JWT token properly in production)
    # For now, this endpoint should be called from your admin script
    
    body = await req.json()
    slug = body.get("slug")
    
    if not slug:
        raise HTTPException(status_code=400, detail="slug required")
    
    # Check if exists
    existing = supabase.table("global_tools").select("id").eq("slug", slug).execute()
    
    tool_data = {
        "slug": slug,
        "name": body.get("name", slug.title()),
        "description": body.get("description", ""),
        "system_prompt": body.get("system_prompt", ""),
        "model": body.get("model", "llama-3.1-8b-instant"),
        "requires_file": body.get("requires_file", False),
        "active": body.get("active", True)
    }
    
    if existing.data:
        # Update
        supabase.table("global_tools").update(tool_data).eq("slug", slug).execute()
        return {"status": "updated", "slug": slug}
    else:
        # Insert
        supabase.table("global_tools").insert(tool_data).execute()
        return {"status": "created", "slug": slug}


@app.delete("/admin/tools/{slug}")
async def delete_tool(slug: str):
    """Deactivate a tool (soft delete)."""
    supabase.table("global_tools").update({"active": False}).eq("slug", slug).execute()
    return {"status": "deactivated", "slug": slug}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)