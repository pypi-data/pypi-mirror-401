-- Enable pgcrypto extension for encryption
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Create user_secrets table with encrypted values
CREATE TABLE IF NOT EXISTS user_secrets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    encrypted_value TEXT NOT NULL,  -- Encrypted with pgcrypto
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, name)
);

-- Create index
CREATE INDEX IF NOT EXISTS idx_user_secrets_user_id ON user_secrets(user_id);

-- Enable RLS
ALTER TABLE user_secrets ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own secret names (not values directly)
CREATE POLICY "Users can view own secrets" ON user_secrets
    FOR SELECT USING (auth.uid() = user_id);

-- Policy: Users can insert their own secrets
CREATE POLICY "Users can insert own secrets" ON user_secrets
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policy: Users can update their own secrets
CREATE POLICY "Users can update own secrets" ON user_secrets
    FOR UPDATE USING (auth.uid() = user_id);

-- Policy: Users can delete their own secrets
CREATE POLICY "Users can delete own secrets" ON user_secrets
    FOR DELETE USING (auth.uid() = user_id);

-- Function to store secret (encrypts server-side)
-- The encryption key should be set as a Supabase secret/env var
CREATE OR REPLACE FUNCTION store_secret(
    p_user_id UUID,
    p_name TEXT,
    p_value TEXT
) RETURNS VOID AS $$
DECLARE
    encryption_key TEXT;
BEGIN
    -- Get encryption key from Supabase secrets
    -- In production, use: SELECT current_setting('app.encryption_key', true);
    encryption_key := 'aniate_secret_key_2026';  -- Change this in production!
    
    INSERT INTO user_secrets (user_id, name, encrypted_value, updated_at)
    VALUES (
        p_user_id,
        p_name,
        encode(pgp_sym_encrypt(p_value, encryption_key), 'base64'),
        NOW()
    )
    ON CONFLICT (user_id, name) 
    DO UPDATE SET 
        encrypted_value = encode(pgp_sym_encrypt(p_value, encryption_key), 'base64'),
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get secret (decrypts server-side)
CREATE OR REPLACE FUNCTION get_secret(
    p_user_id UUID,
    p_name TEXT
) RETURNS TEXT AS $$
DECLARE
    encrypted TEXT;
    encryption_key TEXT;
BEGIN
    -- Verify user owns this secret
    IF p_user_id != auth.uid() THEN
        RETURN NULL;
    END IF;
    
    encryption_key := 'aniate_secret_key_2026';  -- Change this in production!
    
    SELECT encrypted_value INTO encrypted
    FROM user_secrets
    WHERE user_id = p_user_id AND name = p_name;
    
    IF encrypted IS NULL THEN
        RETURN NULL;
    END IF;
    
    RETURN pgp_sym_decrypt(decode(encrypted, 'base64'), encryption_key);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant execute permissions
GRANT EXECUTE ON FUNCTION store_secret TO authenticated;
GRANT EXECUTE ON FUNCTION get_secret TO authenticated;
