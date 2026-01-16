-- =============================================================================
-- ANIATE SUPABASE SCHEMA v1.2.5
-- Run these in ORDER in your Supabase SQL editor
-- =============================================================================

-- ============================================
-- STEP 1: Create profiles table FIRST
-- Run this BEFORE anything else
-- ============================================
CREATE TABLE IF NOT EXISTS public.profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE,
    email TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Make username optional initially (can be NULL)
-- Users will set username on first login via app

-- Index for fast username lookups
CREATE INDEX IF NOT EXISTS idx_profiles_username ON public.profiles(username);

-- RLS for profiles
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Drop existing policies first to avoid conflicts
DROP POLICY IF EXISTS "Profiles are viewable by everyone" ON public.profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON public.profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON public.profiles;

-- Anyone can read profiles (for marketplace)
CREATE POLICY "Profiles are viewable by everyone" ON public.profiles
    FOR SELECT USING (true);

-- Users can only update their own profile
CREATE POLICY "Users can update own profile" ON public.profiles
    FOR UPDATE USING (auth.uid() = id);

-- Users can insert their own profile
CREATE POLICY "Users can insert own profile" ON public.profiles
    FOR INSERT WITH CHECK (auth.uid() = id);


-- ============================================
-- STEP 2: Create trigger AFTER profiles table exists
-- This auto-creates profile on signup
-- ============================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    -- Create a profile entry with just id and email
    -- Username will be NULL initially, user sets it via app
    INSERT INTO public.profiles (id, email)
    VALUES (NEW.id, NEW.email)
    ON CONFLICT (id) DO NOTHING;
    
    RETURN NEW;
EXCEPTION WHEN OTHERS THEN
    -- Don't fail signup if profile creation fails
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop and recreate trigger
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();


-- ============================================
-- STEP 3: Marketplace table
-- ============================================
CREATE TABLE IF NOT EXISTS public.marketplace (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    slug TEXT NOT NULL,
    
    -- Assistant config
    role TEXT,
    speaking_style TEXT,
    tone TEXT,
    formality TEXT,
    length TEXT,
    things_to_avoid TEXT,
    
    -- Metadata
    installs INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(user_id, slug),
    UNIQUE(username, slug)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_marketplace_username ON public.marketplace(username);
CREATE INDEX IF NOT EXISTS idx_marketplace_slug ON public.marketplace(slug);
CREATE INDEX IF NOT EXISTS idx_marketplace_installs ON public.marketplace(installs DESC);

-- RLS
ALTER TABLE public.marketplace ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Marketplace is viewable by everyone" ON public.marketplace;
DROP POLICY IF EXISTS "Users can insert own marketplace items" ON public.marketplace;
DROP POLICY IF EXISTS "Users can update own marketplace items" ON public.marketplace;
DROP POLICY IF EXISTS "Users can delete own marketplace items" ON public.marketplace;

CREATE POLICY "Marketplace is viewable by everyone" ON public.marketplace
    FOR SELECT USING (true);

CREATE POLICY "Users can insert own marketplace items" ON public.marketplace
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own marketplace items" ON public.marketplace
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own marketplace items" ON public.marketplace
    FOR DELETE USING (auth.uid() = user_id);


-- ============================================
-- STEP 4: Update assistants table (add source)
-- ============================================
DO $$ 
BEGIN
    ALTER TABLE public.assistants ADD COLUMN IF NOT EXISTS source TEXT;
EXCEPTION WHEN OTHERS THEN
    NULL;
END $$;


-- ============================================
-- STEP 5: Update marketplace timestamp trigger
-- ============================================
CREATE OR REPLACE FUNCTION public.update_marketplace_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS marketplace_updated_at ON public.marketplace;
CREATE TRIGGER marketplace_updated_at
    BEFORE UPDATE ON public.marketplace
    FOR EACH ROW EXECUTE FUNCTION public.update_marketplace_timestamp();


-- ============================================
-- STEP 6: Helpful view for popular brews
-- ============================================
CREATE OR REPLACE VIEW public.popular_brews AS
SELECT 
    m.username,
    m.slug,
    m.role,
    m.installs,
    m.created_at
FROM public.marketplace m
ORDER BY m.installs DESC
LIMIT 100;


-- ============================================
-- DONE! 
-- 
-- Tables created:
-- - profiles (id, username, email, created_at)
-- - marketplace (for sharing brews)
--
-- The trigger will auto-create profile on signup.
-- Username is NULL initially - user sets it via app.
-- ============================================
