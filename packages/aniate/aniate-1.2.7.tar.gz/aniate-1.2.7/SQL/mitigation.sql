-- ==============================================================================
-- 1. PROFILES (Users + Metrics)
-- ==============================================================================
create table public.profiles (
  id uuid references auth.users on delete cascade primary key,
  email text,
  plan text default 'hobby' check (plan in ('hobby', 'pro')),
  
  -- METRICS (Auto-updated via triggers)
  assistants_count int default 0,
  chats_count int default 0,
  total_tokens_used bigint default 0,
  
  created_at timestamp with time zone default timezone('utc'::text, now())
);

alter table public.profiles enable row level security;
create policy "Users see own profile" on public.profiles for select using (auth.uid() = id);

-- TRIGGER: Create profile on Signup
create or replace function public.handle_new_user() returns trigger as $$
begin
  insert into public.profiles (id, email) values (new.id, new.email);
  return new;
end;
$$ language plpgsql security definer;
create trigger on_auth_user_created after insert on auth.users for each row execute procedure public.handle_new_user();


-- ==============================================================================
-- 2. ASSISTANTS (The Brains - Now with Specific Traits)
-- ==============================================================================
create table public.assistants (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  
  slug text not null, -- The command name (e.g. 'kabir', 'gf')
  
  -- The Core Instructions
  role text not null, -- "You are a senior python engineer"
  
  -- The Specific Traits (Your request)
  length text default 'concise',        -- "Short", "Long", "1 paragraph"
  speaking_style text default 'direct', -- "Sarcastic", "Humble", "Dry"
  tone text default 'neutral',          -- "Professional", "Casual"
  formality text default 'standard',    -- "Formal", "Slang", "No punctuation"
  things_to_avoid text,                 -- "No emojis, no moralizing, no fluff"
  
  -- Computed System Prompt (Optional, or constructed in Python)
  -- We'll just construct it in Python using the fields above.
  
  created_at timestamp with time zone default timezone('utc'::text, now()),
  unique(user_id, slug)
);

alter table public.assistants enable row level security;
create policy "Users manage own assistants" on public.assistants for all using (auth.uid() = user_id);

-- TRIGGER: Auto-increment 'assistants_count'
create or replace function public.increment_assistants() returns trigger as $$
begin
  update public.profiles set assistants_count = assistants_count + 1 where id = new.user_id;
  return new;
end;
$$ language plpgsql security definer;
create trigger on_assistant_created after insert on public.assistants for each row execute procedure public.increment_assistants();


-- ==============================================================================
-- 3. SESSIONS (Chat History + TTL)
-- ==============================================================================
create table public.sessions (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  assistant_id uuid references public.assistants(id) on delete cascade not null,
  
  session_name text not null,
  messages jsonb not null default '[]'::jsonb,
  
  expires_at timestamp with time zone default (now() + interval '7 days'), 
  created_at timestamp with time zone default timezone('utc'::text, now()),
  
  unique(user_id, assistant_id, session_name)
);

alter table public.sessions enable row level security;
create policy "Users manage sessions" on public.sessions for all using (auth.uid() = user_id);

-- TRIGGER: Auto-increment 'chats_count'
create or replace function public.increment_chats() returns trigger as $$
begin
  update public.profiles set chats_count = chats_count + 1 where id = new.user_id;
  return new;
end;
$$ language plpgsql security definer;
create trigger on_session_created after insert on public.sessions for each row execute procedure public.increment_chats();