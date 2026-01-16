-- =============================================================================
-- ANIATE SUPABASE SCHEMA v1.2.4
-- Run this in your Supabase SQL editor to set up marketplace support
-- =============================================================================

-- ============================================
-- 1. PROFILES TABLE (for usernames)
-- Must be created FIRST before trigger
-- ============================================
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT UNIQUE NOT NULL,
    email TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Constraints
    CONSTRAINT username_length CHECK (char_length(username) >= 3),
    CONSTRAINT username_format CHECK (username ~ '^[a-z0-9_]+$')
);

-- Index for fast username lookups
CREATE INDEX IF NOT EXISTS idx_profiles_username ON profiles(username);

-- RLS for profiles
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Drop existing policies first to avoid conflicts
DROP POLICY IF EXISTS "Profiles are viewable by everyone" ON profiles;
DROP POLICY IF EXISTS "Users can update own profile" ON profiles;
DROP POLICY IF EXISTS "Users can insert own profile" ON profiles;

-- Anyone can read profiles (for marketplace)
CREATE POLICY "Profiles are viewable by everyone" ON profiles
    FOR SELECT USING (true);

-- Users can only update their own profile
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Users can insert their own profile
CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = id);


-- ============================================
-- 2. MARKETPLACE TABLE
-- ============================================
CREATE TABLE IF NOT EXISTS marketplace (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    slug TEXT NOT NULL,
    
    -- Assistant config (same as assistants table)
    role TEXT,
    speaking_style TEXT,
    tone TEXT,
    formality TEXT,
    length TEXT,
    things_to_avoid TEXT,
    
    -- Marketplace metadata
    installs INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Unique constraint: one brew per user per name
    UNIQUE(user_id, slug),
    UNIQUE(username, slug)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_marketplace_username ON marketplace(username);
CREATE INDEX IF NOT EXISTS idx_marketplace_slug ON marketplace(slug);
CREATE INDEX IF NOT EXISTS idx_marketplace_installs ON marketplace(installs DESC);

-- RLS for marketplace
ALTER TABLE marketplace ENABLE ROW LEVEL SECURITY;

-- Drop existing policies first
DROP POLICY IF EXISTS "Marketplace is viewable by everyone" ON marketplace;
DROP POLICY IF EXISTS "Users can insert own marketplace items" ON marketplace;
DROP POLICY IF EXISTS "Users can update own marketplace items" ON marketplace;
DROP POLICY IF EXISTS "Users can delete own marketplace items" ON marketplace;

-- Anyone can read marketplace
CREATE POLICY "Marketplace is viewable by everyone" ON marketplace
    FOR SELECT USING (true);

-- Users can only modify their own listings
CREATE POLICY "Users can insert own marketplace items" ON marketplace
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own marketplace items" ON marketplace
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own marketplace items" ON marketplace
    FOR DELETE USING (auth.uid() = user_id);


-- ============================================
-- 3. UPDATE ASSISTANTS TABLE (add source tracking)
-- ============================================
ALTER TABLE assistants ADD COLUMN IF NOT EXISTS source TEXT;
-- source tracks where the brew came from, e.g., "@kabir" if installed from marketplace


-- ============================================
-- 4. TRIGGER: Auto-create profile on signup
-- NOTE: This only works if user signs up through the app
-- which passes username in metadata. For existing users,
-- profiles should be created manually or through the app.
-- ============================================
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
DECLARE
    new_username TEXT;
BEGIN
    -- Get username from metadata, or generate a fallback
    new_username := COALESCE(
        NEW.raw_user_meta_data->>'username', 
        'user_' || substring(NEW.id::text, 1, 8)
    );
    
    -- Only insert if profiles table exists and username is valid
    IF char_length(new_username) >= 3 THEN
        INSERT INTO public.profiles (id, username, email)
        VALUES (NEW.id, new_username, NEW.email)
        ON CONFLICT (id) DO NOTHING;
    END IF;
    
    RETURN NEW;
EXCEPTION WHEN OTHERS THEN
    -- Silently fail if profile creation fails
    -- User can create profile later through app
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Drop existing trigger if exists, then create
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();


-- ============================================
-- 5. TRIGGER: Update marketplace timestamp
-- ============================================
CREATE OR REPLACE FUNCTION update_marketplace_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS marketplace_updated_at ON marketplace;
CREATE TRIGGER marketplace_updated_at
    BEFORE UPDATE ON marketplace
    FOR EACH ROW EXECUTE FUNCTION update_marketplace_timestamp();


-- ============================================
-- 6. HELPFUL VIEWS
-- ============================================

-- Top brews view
CREATE OR REPLACE VIEW popular_brews AS
SELECT 
    m.username,
    m.slug,
    m.role,
    m.installs,
    m.created_at
FROM marketplace m
ORDER BY m.installs DESC
LIMIT 100;


-- ============================================
-- DONE! Your Supabase is now ready for:
-- - User profiles with usernames
-- - Marketplace for sharing brews
-- - Install tracking
-- ============================================
