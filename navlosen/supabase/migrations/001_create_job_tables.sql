-- NAV-Losen Job Search - Supabase Database Schema
-- Created: 2025-10-30
-- Purpose: Store saved jobs, job alerts, and application history

-- Enable UUID extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- 1. SAVED JOBS TABLE
-- =====================================================
-- Users can bookmark/save job listings for later

CREATE TABLE IF NOT EXISTS saved_jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id VARCHAR(255) NOT NULL,
  job_title VARCHAR(500),
  company_name VARCHAR(500),
  location VARCHAR(255),
  saved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  notes TEXT,
  application_status VARCHAR(50) DEFAULT 'not_applied' CHECK (
    application_status IN ('not_applied', 'applied', 'interview', 'rejected', 'accepted')
  ),
  tags TEXT[],
  job_data JSONB, -- Store full job data from API
  UNIQUE(user_id, job_id)
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_saved_jobs_user_id ON saved_jobs(user_id);
CREATE INDEX IF NOT EXISTS idx_saved_jobs_status ON saved_jobs(application_status);
CREATE INDEX IF NOT EXISTS idx_saved_jobs_saved_at ON saved_jobs(saved_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE saved_jobs ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Users can only see their own saved jobs
CREATE POLICY "Users can view own saved jobs"
  ON saved_jobs FOR SELECT
  USING (auth.uid() = user_id);

-- RLS Policy: Users can insert their own saved jobs
CREATE POLICY "Users can insert own saved jobs"
  ON saved_jobs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- RLS Policy: Users can update their own saved jobs
CREATE POLICY "Users can update own saved jobs"
  ON saved_jobs FOR UPDATE
  USING (auth.uid() = user_id);

-- RLS Policy: Users can delete their own saved jobs
CREATE POLICY "Users can delete own saved jobs"
  ON saved_jobs FOR DELETE
  USING (auth.uid() = user_id);

-- =====================================================
-- 2. JOB ALERTS TABLE
-- =====================================================
-- Users can set up alerts for new jobs matching their criteria

CREATE TABLE IF NOT EXISTS job_alerts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  search_criteria JSONB NOT NULL,
  frequency VARCHAR(20) NOT NULL DEFAULT 'daily' CHECK (
    frequency IN ('realtime', 'daily', 'weekly')
  ),
  active BOOLEAN DEFAULT TRUE,
  last_sent_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_job_alerts_user_id ON job_alerts(user_id);
CREATE INDEX IF NOT EXISTS idx_job_alerts_active ON job_alerts(active);

-- Enable Row Level Security (RLS)
ALTER TABLE job_alerts ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Users can only see their own alerts
CREATE POLICY "Users can view own job alerts"
  ON job_alerts FOR SELECT
  USING (auth.uid() = user_id);

-- RLS Policy: Users can insert their own alerts
CREATE POLICY "Users can insert own job alerts"
  ON job_alerts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- RLS Policy: Users can update their own alerts
CREATE POLICY "Users can update own job alerts"
  ON job_alerts FOR UPDATE
  USING (auth.uid() = user_id);

-- RLS Policy: Users can delete their own alerts
CREATE POLICY "Users can delete own job alerts"
  ON job_alerts FOR DELETE
  USING (auth.uid() = user_id);

-- =====================================================
-- 3. APPLICATION HISTORY TABLE
-- =====================================================
-- Track job applications sent by users

CREATE TABLE IF NOT EXISTS application_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  job_id VARCHAR(255) NOT NULL,
  company VARCHAR(255),
  position VARCHAR(255),
  applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  status VARCHAR(50) DEFAULT 'applied' CHECK (
    status IN ('applied', 'viewed', 'interview_scheduled', 'interview_completed', 'rejected', 'accepted', 'withdrawn')
  ),
  notes TEXT,
  interview_date TIMESTAMP WITH TIME ZONE,
  response_date TIMESTAMP WITH TIME ZONE,
  application_method VARCHAR(50), -- 'gmail', 'email', 'website', 'in_person'
  email_thread_id VARCHAR(255), -- Gmail thread ID if sent via Gmail
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_application_history_user_id ON application_history(user_id);
CREATE INDEX IF NOT EXISTS idx_application_history_status ON application_history(status);
CREATE INDEX IF NOT EXISTS idx_application_history_applied_at ON application_history(applied_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE application_history ENABLE ROW LEVEL SECURITY;

-- RLS Policy: Users can only see their own application history
CREATE POLICY "Users can view own application history"
  ON application_history FOR SELECT
  USING (auth.uid() = user_id);

-- RLS Policy: Users can insert their own applications
CREATE POLICY "Users can insert own applications"
  ON application_history FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- RLS Policy: Users can update their own applications
CREATE POLICY "Users can update own applications"
  ON application_history FOR UPDATE
  USING (auth.uid() = user_id);

-- RLS Policy: Users can delete their own applications
CREATE POLICY "Users can delete own applications"
  ON application_history FOR DELETE
  USING (auth.uid() = user_id);

-- =====================================================
-- 4. FUNCTIONS AND TRIGGERS
-- =====================================================

-- Function to update 'updated_at' timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for job_alerts table
CREATE TRIGGER update_job_alerts_updated_at
  BEFORE UPDATE ON job_alerts
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Trigger for application_history table
CREATE TRIGGER update_application_history_updated_at
  BEFORE UPDATE ON application_history
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- 5. HELPER VIEWS
-- =====================================================

-- View: Recent saved jobs with application status
CREATE OR REPLACE VIEW v_recent_saved_jobs AS
SELECT
  sj.id,
  sj.user_id,
  sj.job_id,
  sj.job_title,
  sj.company_name,
  sj.location,
  sj.saved_at,
  sj.application_status,
  sj.tags,
  ah.applied_at,
  ah.status AS current_application_status
FROM saved_jobs sj
LEFT JOIN application_history ah ON sj.job_id = ah.job_id AND sj.user_id = ah.user_id
ORDER BY sj.saved_at DESC;

-- View: User job search statistics
CREATE OR REPLACE VIEW v_user_job_stats AS
SELECT
  user_id,
  COUNT(DISTINCT job_id) AS total_saved_jobs,
  COUNT(DISTINCT CASE WHEN application_status != 'not_applied' THEN job_id END) AS jobs_applied_to,
  COUNT(DISTINCT CASE WHEN application_status = 'interview' THEN job_id END) AS interviews_scheduled,
  COUNT(DISTINCT CASE WHEN application_status = 'accepted' THEN job_id END) AS job_offers_received
FROM saved_jobs
GROUP BY user_id;

-- =====================================================
-- 6. SEED DATA (Optional - for testing)
-- =====================================================

-- You can add test data here if needed
-- Example:
-- INSERT INTO saved_jobs (user_id, job_id, job_title, company_name, location, notes, tags)
-- VALUES (
--   'YOUR_USER_ID_HERE',
--   'mock-1',
--   'Helsefagarbeider',
--   'Oslo Kommune',
--   'Oslo',
--   'Interessant stilling, skal søke denne uken',
--   ARRAY['helse', 'heltid', 'prioritet']
-- );

-- =====================================================
-- 7. GRANTS (for service_role access if needed)
-- =====================================================

-- Grant permissions to authenticated users
GRANT ALL ON saved_jobs TO authenticated;
GRANT ALL ON job_alerts TO authenticated;
GRANT ALL ON application_history TO authenticated;

-- Grant permissions to anon for read-only access to views
GRANT SELECT ON v_recent_saved_jobs TO anon;
GRANT SELECT ON v_user_job_stats TO anon;

-- =====================================================
-- MIGRATION COMPLETE
-- =====================================================

-- To verify tables were created:
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- To verify RLS policies:
-- SELECT tablename, policyname FROM pg_policies WHERE schemaname = 'public';

COMMIT;
