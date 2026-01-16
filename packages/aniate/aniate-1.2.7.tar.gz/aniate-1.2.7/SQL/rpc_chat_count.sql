-- Create RPC function to increment chat count and track tokens
-- This is called from Python after every Groq API call

create or replace function public.increment_user_chat_count(user_id uuid, tokens_used int default 0)
returns void as $$
begin
  update public.profiles 
  set chats_count = chats_count + 1,
      total_tokens_used = total_tokens_used + tokens_used
  where id = user_id;
end;
$$ language plpgsql security definer;

-- Reset your current count to 0 so it starts fresh
update public.profiles set chats_count = 0, total_tokens_used = 0;
