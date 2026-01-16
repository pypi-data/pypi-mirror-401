-- Migration: Split token tracking into input/output/total
-- Run this in Supabase SQL Editor

-- 1. Drop old column
ALTER TABLE public.profiles DROP COLUMN IF EXISTS total_tokens_used;

-- 2. Add new token columns
ALTER TABLE public.profiles 
  ADD COLUMN input_tokens bigint default 0,
  ADD COLUMN output_tokens bigint default 0,
  ADD COLUMN total_tokens bigint default 0;

-- 3. Update RPC function to track separate token counts
CREATE OR REPLACE FUNCTION public.increment_user_chat_count(
  user_id uuid, 
  prompt_tokens int default 0,
  completion_tokens int default 0
)
RETURNS void AS $$
DECLARE
  total int;
BEGIN
  total := prompt_tokens + completion_tokens;
  
  UPDATE public.profiles 
  SET chats_count = chats_count + 1,
      input_tokens = input_tokens + prompt_tokens,
      output_tokens = output_tokens + completion_tokens,
      total_tokens = total_tokens + total
  WHERE id = user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
