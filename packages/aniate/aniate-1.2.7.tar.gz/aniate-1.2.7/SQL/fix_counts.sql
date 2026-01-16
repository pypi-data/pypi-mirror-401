-- Fix for assistants_count and chats_count tracking

-- ==============================================================================
-- FIX: Add DECREMENT trigger for assistants
-- ==============================================================================
create or replace function public.decrement_assistants() returns trigger as $$
begin
  update public.profiles set assistants_count = assistants_count - 1 where id = old.user_id;
  return old;
end;
$$ language plpgsql security definer;

create trigger on_assistant_deleted 
  after delete on public.assistants 
  for each row execute procedure public.decrement_assistants();


-- ==============================================================================
-- FIX: Add DECREMENT trigger for sessions (optional - if you want to track deletes)
-- ==============================================================================
create or replace function public.decrement_chats() returns trigger as $$
begin
  update public.profiles set chats_count = chats_count - 1 where id = old.user_id;
  return old;
end;
$$ language plpgsql security definer;

create trigger on_session_deleted 
  after delete on public.sessions 
  for each row execute procedure public.decrement_chats();


-- ==============================================================================
-- MANUAL FIX: Recalculate counts for existing data
-- ==============================================================================

-- Fix assistants_count (count actual assistants)
update public.profiles 
set assistants_count = (
  select count(*) 
  from public.assistants 
  where assistants.user_id = profiles.id
);

-- Fix chats_count (count actual sessions)
update public.profiles 
set chats_count = (
  select count(*) 
  from public.sessions 
  where sessions.user_id = profiles.id
);
