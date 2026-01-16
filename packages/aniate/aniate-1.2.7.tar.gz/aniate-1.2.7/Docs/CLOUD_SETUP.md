# Cloud Storage Setup Instructions

## Supabase Dashboard Setup

### 1. Create Storage Bucket
1. Go to Supabase Dashboard → Storage
2. Click "New Bucket"
3. Name: `user-files`
4. Public: **NO** (private bucket)
5. File size limit: 50MB (or your preference)
6. Allowed MIME types: Leave empty for all types

### 2. Set Storage Policies
Navigate to Storage → user-files → Policies

**Policy 1: Users can upload own files**
```sql
CREATE POLICY "Users can upload own files" ON storage.objects
FOR INSERT TO authenticated
WITH CHECK (bucket_id = 'user-files' AND (storage.foldername(name))[1] = auth.uid()::text);
```

**Policy 2: Users can read own files**
```sql
CREATE POLICY "Users can read own files" ON storage.objects
FOR SELECT TO authenticated
USING (bucket_id = 'user-files' AND (storage.foldername(name))[1] = auth.uid()::text);
```

**Policy 3: Users can update own files**
```sql
CREATE POLICY "Users can update own files" ON storage.objects
FOR UPDATE TO authenticated
USING (bucket_id = 'user-files' AND (storage.foldername(name))[1] = auth.uid()::text);
```

**Policy 4: Users can delete own files**
```sql
CREATE POLICY "Users can delete own files" ON storage.objects
FOR DELETE TO authenticated
USING (bucket_id = 'user-files' AND (storage.foldername(name))[1] = auth.uid()::text);
```

### 3. Create Database Table
Navigate to SQL Editor → Run the migration:
```bash
cat migrations/create_user_files_table.sql
```
Copy and paste into SQL Editor, then Execute.

## Verify Setup
```bash
ant files  # Should show empty list or your files
ant save test.txt  # Upload a test file
ant files  # Should show the uploaded file
ant fetch test.txt  # Download it back
```

## Storage Structure
```
user-files/
  └── {user_id}/
      ├── report.pdf
      ├── screenshot.png
      └── notes.txt
```

Each user's files are isolated in their own folder using their UUID.
