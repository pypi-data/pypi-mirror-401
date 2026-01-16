-- =============================================================================
-- ANIATE SUPABASE SCHEMA v1.2.6
-- 
-- IMPORTANT: Run each section SEPARATELY in Supabase SQL Editor
-- Copy-paste one section at a time and run it before moving to next
-- =============================================================================


-- =============================================================================
-- SECTION 1: DROP OLD TRIGGER (Run this FIRST)
-- =============================================================================
-- The old trigger might be causing the "username does not exist" error
-- because it references columns that don't exist

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
DROP FUNCTION IF EXISTS public.handle_new_user();

-- After running this, you should see "Success. No rows returned"


-- =============================================================================
-- SECTION 2: CREATE/UPDATE PROFILES TABLE (Run this SECOND)
-- =============================================================================
-- This creates the profiles table if it doesn't exist
-- Or adds missing columns if it does exist

-- Create table if not exists
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT,
    username TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add username column if it's missing (for existing tables)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name = 'profiles' 
        AND column_name = 'username'
    ) THEN
        ALTER TABLE public.profiles ADD COLUMN username TEXT;
    END IF;
END $$;

-- Create unique index on username (allows NULL values)
DROP INDEX IF EXISTS idx_profiles_username;
CREATE UNIQUE INDEX idx_profiles_username ON public.profiles(username) WHERE username IS NOT NULL;

-- After running this, you should see "Success. No rows returned"


-- =============================================================================
-- SECTION 3: SET UP RLS FOR PROFILES (Run this THIRD)
-- =============================================================================

ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "profiles_select_all" ON public.profiles;
DROP POLICY IF EXISTS "profiles_insert_own" ON public.profiles;
DROP POLICY IF EXISTS "profiles_update_own" ON public.profiles;

CREATE POLICY "profiles_select_all" ON public.profiles FOR SELECT USING (true);
CREATE POLICY "profiles_insert_own" ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);
CREATE POLICY "profiles_update_own" ON public.profiles FOR UPDATE USING (auth.uid() = id);

-- After running this, you should see "Success. No rows returned"


-- =============================================================================
-- SECTION 4: CREATE NEW TRIGGER (Run this FOURTH)
-- =============================================================================
-- This trigger auto-creates a profile when a user signs up
-- It only inserts id and email - username will be set by the app later

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
    -- Log error but don't fail the signup
    RAISE WARNING 'Failed to create profile for user %: %', NEW.id, SQLERRM;
    RETURN NEW;
END;
$$;

CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();

-- After running this, you should see "Success. No rows returned"


-- =============================================================================
-- SECTION 5: CREATE MARKETPLACE TABLE (Run this FIFTH)
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.marketplace (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    slug TEXT NOT NULL,
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

CREATE INDEX IF NOT EXISTS idx_marketplace_username ON public.marketplace(username);
CREATE INDEX IF NOT EXISTS idx_marketplace_slug ON public.marketplace(slug);
CREATE INDEX IF NOT EXISTS idx_marketplace_installs ON public.marketplace(installs DESC);

-- After running this, you should see "Success. No rows returned"


-- =============================================================================
-- SECTION 6: SET UP RLS FOR MARKETPLACE (Run this SIXTH)
-- =============================================================================

ALTER TABLE public.marketplace ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "marketplace_select_all" ON public.marketplace;
DROP POLICY IF EXISTS "marketplace_insert_own" ON public.marketplace;
DROP POLICY IF EXISTS "marketplace_update_own" ON public.marketplace;
DROP POLICY IF EXISTS "marketplace_delete_own" ON public.marketplace;

CREATE POLICY "marketplace_select_all" ON public.marketplace FOR SELECT USING (true);
CREATE POLICY "marketplace_insert_own" ON public.marketplace FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "marketplace_update_own" ON public.marketplace FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "marketplace_delete_own" ON public.marketplace FOR DELETE USING (auth.uid() = user_id);

-- After running this, you should see "Success. No rows returned"


-- =============================================================================
-- SECTION 7: ADD SOURCE COLUMN TO ASSISTANTS (Run this SEVENTH)
-- =============================================================================

DO $$ 
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'assistants') THEN
        IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns 
            WHERE table_name = 'assistants' AND column_name = 'source'
        ) THEN
            ALTER TABLE public.assistants ADD COLUMN source TEXT;
        END IF;
    END IF;
END $$;

-- After running this, you should see "Success. No rows returned"


-- =============================================================================
-- SECTION 8: TEST THE SETUP (Run this LAST to verify)
-- =============================================================================

-- This should return the profiles table structure
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_schema = 'public' AND table_name = 'profiles'
ORDER BY ordinal_position;

-- Expected output:
-- id        | uuid                        | NO
-- email     | text                        | YES
-- username  | text                        | YES
-- created_at| timestamp with time zone    | YES


-- =============================================================================
-- DONE!
-- 
-- If any section fails, fix that section before continuing.
-- The most common issue is the old trigger - Section 1 drops it.
-- =============================================================================
