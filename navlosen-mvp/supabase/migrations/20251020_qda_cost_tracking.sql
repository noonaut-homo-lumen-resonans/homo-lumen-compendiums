/**
 * QDA v2.0 - Cost Tracking Migration
 * 
 * Creates tables and views for tracking QDA usage and costs
 * 
 * @version 2.0
 * @date 2025-10-20
 */

-- ============================================================================
-- TABLE: qda_usage
-- Logs every QDA query with detailed layer information
-- ============================================================================

CREATE TABLE IF NOT EXISTS homo_lumen_data.qda_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  
  -- User context
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  session_id UUID,
  
  -- Query details
  message TEXT NOT NULL,
  quadrant TEXT,
  emotion TEXT,
  stress_level INTEGER CHECK (stress_level >= 0 AND stress_level <= 10),
  polyvagal_state TEXT CHECK (polyvagal_state IN ('dorsal', 'sympathetic', 'ventral')),
  
  -- Response details
  final_response TEXT NOT NULL,
  highest_layer_used TEXT NOT NULL,
  complexity_score DECIMAL(3, 2) CHECK (complexity_score >= 0 AND complexity_score <= 1),
  
  -- Cost tracking
  total_cost DECIMAL(10, 6) NOT NULL,
  total_time INTEGER NOT NULL, -- milliseconds
  
  -- Layer breakdown (JSONB for flexibility)
  layers JSONB NOT NULL,
  
  -- Metadata
  agent_name TEXT DEFAULT 'Lira',
  environment TEXT DEFAULT 'production' CHECK (environment IN ('development', 'staging', 'production'))
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_qda_usage_user_id ON homo_lumen_data.qda_usage(user_id);
CREATE INDEX IF NOT EXISTS idx_qda_usage_created_at ON homo_lumen_data.qda_usage(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_qda_usage_session_id ON homo_lumen_data.qda_usage(session_id);
CREATE INDEX IF NOT EXISTS idx_qda_usage_polyvagal_state ON homo_lumen_data.qda_usage(polyvagal_state);
CREATE INDEX IF NOT EXISTS idx_qda_usage_highest_layer ON homo_lumen_data.qda_usage(highest_layer_used);

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

ALTER TABLE homo_lumen_data.qda_usage ENABLE ROW LEVEL SECURITY;

-- Users can only see their own QDA queries
CREATE POLICY "Users can view their own QDA usage"
  ON homo_lumen_data.qda_usage
  FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own QDA queries
CREATE POLICY "Users can insert their own QDA usage"
  ON homo_lumen_data.qda_usage
  FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Admins can view all QDA queries (for analytics)
CREATE POLICY "Admins can view all QDA usage"
  ON homo_lumen_data.qda_usage
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM nav_losen_data.users
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- ============================================================================
-- VIEW: qda_daily_cost_per_user
-- Aggregates daily cost per user
-- ============================================================================

CREATE OR REPLACE VIEW homo_lumen_data.qda_daily_cost_per_user AS
SELECT
  user_id,
  DATE(created_at) AS date,
  COUNT(*) AS query_count,
  SUM(total_cost) AS total_cost,
  AVG(total_cost) AS avg_cost_per_query,
  AVG(total_time) AS avg_time_per_query,
  AVG(complexity_score) AS avg_complexity,
  
  -- Layer activation rates
  SUM(CASE WHEN highest_layer_used = 'Strategen' THEN 1 ELSE 0 END) AS strategen_activations,
  SUM(CASE WHEN highest_layer_used = 'Utforskeren' THEN 1 ELSE 0 END) AS utforskeren_activations,
  
  -- Polyvagal state distribution
  SUM(CASE WHEN polyvagal_state = 'dorsal' THEN 1 ELSE 0 END) AS dorsal_count,
  SUM(CASE WHEN polyvagal_state = 'sympathetic' THEN 1 ELSE 0 END) AS sympathetic_count,
  SUM(CASE WHEN polyvagal_state = 'ventral' THEN 1 ELSE 0 END) AS ventral_count
FROM homo_lumen_data.qda_usage
GROUP BY user_id, DATE(created_at)
ORDER BY date DESC, user_id;

-- ============================================================================
-- VIEW: qda_system_stats
-- System-wide QDA statistics (admin only)
-- ============================================================================

CREATE OR REPLACE VIEW homo_lumen_data.qda_system_stats AS
SELECT
  COUNT(*) AS total_queries,
  COUNT(DISTINCT user_id) AS unique_users,
  SUM(total_cost) AS total_cost,
  AVG(total_cost) AS avg_cost_per_query,
  AVG(total_time) AS avg_time_per_query,
  AVG(complexity_score) AS avg_complexity,
  
  -- Layer usage
  SUM(CASE WHEN highest_layer_used = 'Vokteren' THEN 1 ELSE 0 END) AS vokteren_count,
  SUM(CASE WHEN highest_layer_used = 'Føleren' THEN 1 ELSE 0 END) AS foleren_count,
  SUM(CASE WHEN highest_layer_used = 'Gjenkjenneren' THEN 1 ELSE 0 END) AS gjenkjenneren_count,
  SUM(CASE WHEN highest_layer_used = 'Utforskeren' THEN 1 ELSE 0 END) AS utforskeren_count,
  SUM(CASE WHEN highest_layer_used = 'Strategen' THEN 1 ELSE 0 END) AS strategen_count,
  SUM(CASE WHEN highest_layer_used = 'Integratoren' THEN 1 ELSE 0 END) AS integratoren_count,
  
  -- Polyvagal distribution
  SUM(CASE WHEN polyvagal_state = 'dorsal' THEN 1 ELSE 0 END) AS dorsal_count,
  SUM(CASE WHEN polyvagal_state = 'sympathetic' THEN 1 ELSE 0 END) AS sympathetic_count,
  SUM(CASE WHEN polyvagal_state = 'ventral' THEN 1 ELSE 0 END) AS ventral_count,
  
  -- Time range
  MIN(created_at) AS first_query,
  MAX(created_at) AS last_query
FROM homo_lumen_data.qda_usage;

-- ============================================================================
-- FUNCTION: log_qda_usage
-- Helper function to log QDA usage from API
-- ============================================================================

CREATE OR REPLACE FUNCTION homo_lumen_data.log_qda_usage(
  p_user_id UUID,
  p_session_id UUID,
  p_message TEXT,
  p_quadrant TEXT,
  p_emotion TEXT,
  p_stress_level INTEGER,
  p_polyvagal_state TEXT,
  p_final_response TEXT,
  p_highest_layer_used TEXT,
  p_complexity_score DECIMAL,
  p_total_cost DECIMAL,
  p_total_time INTEGER,
  p_layers JSONB,
  p_agent_name TEXT DEFAULT 'Lira',
  p_environment TEXT DEFAULT 'production'
)
RETURNS UUID
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_id UUID;
BEGIN
  INSERT INTO homo_lumen_data.qda_usage (
    user_id,
    session_id,
    message,
    quadrant,
    emotion,
    stress_level,
    polyvagal_state,
    final_response,
    highest_layer_used,
    complexity_score,
    total_cost,
    total_time,
    layers,
    agent_name,
    environment
  ) VALUES (
    p_user_id,
    p_session_id,
    p_message,
    p_quadrant,
    p_emotion,
    p_stress_level,
    p_polyvagal_state,
    p_final_response,
    p_highest_layer_used,
    p_complexity_score,
    p_total_cost,
    p_total_time,
    p_layers,
    p_agent_name,
    p_environment
  )
  RETURNING id INTO v_id;
  
  RETURN v_id;
END;
$$;

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE homo_lumen_data.qda_usage IS 'Logs all QDA v2.0 queries with detailed layer information and cost tracking';
COMMENT ON VIEW homo_lumen_data.qda_daily_cost_per_user IS 'Daily aggregated QDA costs per user';
COMMENT ON VIEW homo_lumen_data.qda_system_stats IS 'System-wide QDA statistics (admin only)';
COMMENT ON FUNCTION homo_lumen_data.log_qda_usage IS 'Helper function to log QDA usage from API';

-- ============================================================================
-- DONE
-- ============================================================================

-- Success message
DO $$
BEGIN
  RAISE NOTICE 'QDA v2.0 cost tracking migration completed successfully!';
  RAISE NOTICE 'Created: qda_usage table, 2 views, 1 function, 5 indexes, 3 RLS policies';
END $$;

