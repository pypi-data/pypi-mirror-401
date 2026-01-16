-- =============================================================================
-- ANIATE COMPLETE SUPABASE SCHEMA v1.2.7
-- 
-- Run EACH section in Supabase SQL Editor ONE AT A TIME
-- Wait for success before running the next section
-- =============================================================================


-- =============================================================================
-- SECTION 1: CLEANUP - Drop old triggers and functions
-- =============================================================================
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user();


-- =============================================================================
-- SECTION 2: PROFILES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    username TEXT UNIQUE,
    plan TEXT DEFAULT 'free',
    assistants_count INTEGER DEFAULT 0,
    chats_count INTEGER DEFAULT 0,
    input_tokens BIGINT DEFAULT 0,
    output_tokens BIGINT DEFAULT 0,
    total_tokens BIGINT DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add any missing columns to existing table
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'username') THEN
        ALTER TABLE public.profiles ADD COLUMN username TEXT UNIQUE;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'profiles' AND column_name = 'plan') THEN
        ALTER TABLE public.profiles ADD COLUMN plan TEXT DEFAULT 'free';
    END IF;
END $$;


-- =============================================================================
-- SECTION 3: PROFILES RLS POLICIES (including DELETE)
-- =============================================================================
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "profiles_select" ON public.profiles;
DROP POLICY IF EXISTS "profiles_insert" ON public.profiles;
DROP POLICY IF EXISTS "profiles_update" ON public.profiles;
DROP POLICY IF EXISTS "profiles_delete" ON public.profiles;

CREATE POLICY "profiles_select" ON public.profiles FOR SELECT USING (true);
CREATE POLICY "profiles_insert" ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "profiles_update" ON public.profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "profiles_delete" ON public.profiles FOR DELETE USING (auth.uid() = id);


-- =============================================================================
-- SECTION 4: AUTO-CREATE PROFILE TRIGGER (minimal - just id and email)
-- =============================================================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER 
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    INSERT INTO public.profiles (id, email)
    VALUES (NEW.id, NEW.email)
    ON CONFLICT (id) DO UPDATE SET email = EXCLUDED.email;
    RETURN NEW;
EXCEPTION WHEN OTHERS THEN
    RAISE WARNING 'Profile creation failed for %: %', NEW.id, SQLERRM;
    RETURN NEW;
END;
$$;

CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();


-- =============================================================================
-- SECTION 5: ASSISTANTS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.assistants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    slug TEXT NOT NULL,
    role TEXT,
    speaking_style TEXT,
    tone TEXT,
    formality TEXT,
    length TEXT,
    things_to_avoid TEXT,
    source TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, slug)
);

ALTER TABLE public.assistants ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "assistants_select" ON public.assistants;
DROP POLICY IF EXISTS "assistants_insert" ON public.assistants;
DROP POLICY IF EXISTS "assistants_update" ON public.assistants;
DROP POLICY IF EXISTS "assistants_delete" ON public.assistants;

CREATE POLICY "assistants_select" ON public.assistants FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "assistants_insert" ON public.assistants FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "assistants_update" ON public.assistants FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "assistants_delete" ON public.assistants FOR DELETE USING (auth.uid() = user_id);


-- =============================================================================
-- SECTION 6: SESSIONS TABLE (chat history)
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    assistant_id UUID REFERENCES public.assistants(id) ON DELETE SET NULL,
    title TEXT,
    messages JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.sessions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "sessions_select" ON public.sessions;
DROP POLICY IF EXISTS "sessions_insert" ON public.sessions;
DROP POLICY IF EXISTS "sessions_update" ON public.sessions;
DROP POLICY IF EXISTS "sessions_delete" ON public.sessions;

CREATE POLICY "sessions_select" ON public.sessions FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "sessions_insert" ON public.sessions FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "sessions_update" ON public.sessions FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "sessions_delete" ON public.sessions FOR DELETE USING (auth.uid() = user_id);


-- =============================================================================
-- SECTION 7: USER_FILES TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.user_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    content TEXT,
    mime_type TEXT,
    size_bytes INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, filename)
);

ALTER TABLE public.user_files ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "user_files_select" ON public.user_files;
DROP POLICY IF EXISTS "user_files_insert" ON public.user_files;
DROP POLICY IF EXISTS "user_files_update" ON public.user_files;
DROP POLICY IF EXISTS "user_files_delete" ON public.user_files;

CREATE POLICY "user_files_select" ON public.user_files FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "user_files_insert" ON public.user_files FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "user_files_update" ON public.user_files FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "user_files_delete" ON public.user_files FOR DELETE USING (auth.uid() = user_id);


-- =============================================================================
-- SECTION 8: USER_SECRETS TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.user_secrets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, key)
);

ALTER TABLE public.user_secrets ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "user_secrets_select" ON public.user_secrets;
DROP POLICY IF EXISTS "user_secrets_insert" ON public.user_secrets;
DROP POLICY IF EXISTS "user_secrets_update" ON public.user_secrets;
DROP POLICY IF EXISTS "user_secrets_delete" ON public.user_secrets;

CREATE POLICY "user_secrets_select" ON public.user_secrets FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "user_secrets_insert" ON public.user_secrets FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "user_secrets_update" ON public.user_secrets FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "user_secrets_delete" ON public.user_secrets FOR DELETE USING (auth.uid() = user_id);


-- =============================================================================
-- SECTION 9: MARKETPLACE TABLE
-- =============================================================================
CREATE TABLE IF NOT EXISTS public.marketplace (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    slug TEXT NOT NULL,
    name TEXT,
    description TEXT,
    role TEXT,
    speaking_style TEXT,
    tone TEXT,
    formality TEXT,
    length TEXT,
    things_to_avoid TEXT,
    installs INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, slug),
    UNIQUE(username, slug)
);

ALTER TABLE public.marketplace ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "marketplace_select" ON public.marketplace;
DROP POLICY IF EXISTS "marketplace_insert" ON public.marketplace;
DROP POLICY IF EXISTS "marketplace_update" ON public.marketplace;
DROP POLICY IF EXISTS "marketplace_delete" ON public.marketplace;

-- Anyone can view marketplace (for browsing)
CREATE POLICY "marketplace_select" ON public.marketplace FOR SELECT USING (true);
CREATE POLICY "marketplace_insert" ON public.marketplace FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "marketplace_update" ON public.marketplace FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "marketplace_delete" ON public.marketplace FOR DELETE USING (auth.uid() = user_id);

-- Indexes for faster marketplace searches
CREATE INDEX IF NOT EXISTS idx_marketplace_username ON public.marketplace(username);
CREATE INDEX IF NOT EXISTS idx_marketplace_slug ON public.marketplace(slug);
CREATE INDEX IF NOT EXISTS idx_marketplace_installs ON public.marketplace(installs DESC);


-- =============================================================================
-- SECTION 10: HELPER FUNCTION - Update username in profile
-- =============================================================================
CREATE OR REPLACE FUNCTION public.set_username(new_username TEXT)
RETURNS BOOLEAN
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    UPDATE public.profiles 
    SET username = new_username 
    WHERE id = auth.uid();
    RETURN true;
EXCEPTION WHEN OTHERS THEN
    RETURN false;
END;
$$;


-- =============================================================================
-- SECTION 11: VERIFY SETUP - Run this to check everything
-- =============================================================================
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns c WHERE c.table_name = t.table_name AND c.table_schema = 'public') as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- Expected output:
-- assistants   | 12
-- marketplace  | 15
-- profiles     | 10
-- sessions     | 6
-- user_files   | 6
-- user_secrets | 6


-- =============================================================================
-- DONE!
-- 
-- After running all sections, the delete function should work because
-- we added DELETE policies for all tables.
--
-- Note: Deleting from auth.users requires service_role key (admin).
-- The profiles table has ON DELETE CASCADE, so when auth.users is deleted,
-- profiles will auto-delete. For user-initiated deletion, we delete
-- from tables directly using the DELETE RLS policies.
-- =============================================================================
