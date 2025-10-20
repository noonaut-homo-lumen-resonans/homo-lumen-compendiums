/**
 * Supabase Migration: QDA Cost Tracking
 *
 * Run this in Supabase SQL Editor or add to migrations/
 *
 * Purpose: Track QDA v2.0 usage, costs, and layer activation patterns
 *
 * @version 2.0
 * @date 2025-10-20
 */

-- =============================================================================
-- TABLE: qda_usage
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.qda_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- User & Session
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  session_id UUID,

  -- Query Details
  query_text TEXT NOT NULL,
  query_length INTEGER GENERATED ALWAYS AS (length(query_text)) STORED,

  -- QDA Processing Results
  highest_layer_used VARCHAR(50) NOT NULL,
  layers_activated TEXT[], -- Array of layer names, e.g., ['Vokteren', 'Føleren', ...]

  -- Cost & Performance
  total_cost DECIMAL(10, 6) NOT NULL,
  total_time_ms INTEGER NOT NULL,
  complexity_score DECIMAL(3, 2) NOT NULL,

  -- User State (at time of query)
  stress_level INTEGER CHECK (stress_level BETWEEN 1 AND 10),
  polyvagal_state VARCHAR(20) CHECK (polyvagal_state IN ('dorsal', 'sympathetic', 'ventral')),
  arousal DECIMAL(3, 2) CHECK (arousal BETWEEN 0 AND 1),
  valence DECIMAL(3, 2) CHECK (valence BETWEEN -1 AND 1),

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),

  -- Metadata
  metadata JSONB DEFAULT '{}'::jsonb
);

-- =============================================================================
-- INDEXES
-- =============================================================================

-- Query by user
CREATE INDEX idx_qda_usage_user_id ON public.qda_usage(user_id);

-- Query by session
CREATE INDEX idx_qda_usage_session_id ON public.qda_usage(session_id);

-- Query by timestamp (for analytics)
CREATE INDEX idx_qda_usage_created_at ON public.qda_usage(created_at DESC);

-- Query by highest layer (for cost analysis)
CREATE INDEX idx_qda_usage_highest_layer ON public.qda_usage(highest_layer_used);

-- Query by polyvagal state (for research)
CREATE INDEX idx_qda_usage_polyvagal ON public.qda_usage(polyvagal_state);

-- Composite index for user + date range queries
CREATE INDEX idx_qda_usage_user_date ON public.qda_usage(user_id, created_at DESC);

-- =============================================================================
-- ROW LEVEL SECURITY (RLS)
-- =============================================================================

ALTER TABLE public.qda_usage ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own usage data
CREATE POLICY "Users can view own QDA usage"
  ON public.qda_usage
  FOR SELECT
  USING (auth.uid() = user_id);

-- Policy: Service role can insert (from API)
CREATE POLICY "Service role can insert QDA usage"
  ON public.qda_usage
  FOR INSERT
  WITH CHECK (true); -- Service role bypasses RLS anyway, but explicit is good

-- Policy: Admins can view all usage data
CREATE POLICY "Admins can view all QDA usage"
  ON public.qda_usage
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.user_roles
      WHERE user_id = auth.uid() AND role = 'admin'
    )
  );

-- =============================================================================
-- TABLE: qda_layer_details (Optional - for detailed layer tracking)
-- =============================================================================

CREATE TABLE IF NOT EXISTS public.qda_layer_details (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Foreign key to qda_usage
  qda_usage_id UUID REFERENCES public.qda_usage(id) ON DELETE CASCADE,

  -- Layer Details
  layer_name VARCHAR(50) NOT NULL,
  layer_icon VARCHAR(10),
  layer_index INTEGER NOT NULL, -- Order in processing (1-6)

  -- Processing Results
  processing_time_ms INTEGER NOT NULL,
  cost DECIMAL(10, 6) NOT NULL,
  activated BOOLEAN DEFAULT true,

  -- Layer-specific data (JSON for flexibility)
  layer_data JSONB NOT NULL,

  -- Timestamp
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for querying layer details by qda_usage_id
CREATE INDEX idx_qda_layer_details_usage_id ON public.qda_layer_details(qda_usage_id);

-- Index for analytics by layer name
CREATE INDEX idx_qda_layer_details_layer_name ON public.qda_layer_details(layer_name);

-- RLS for layer details (inherit from qda_usage)
ALTER TABLE public.qda_layer_details ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own QDA layer details"
  ON public.qda_layer_details
  FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM public.qda_usage
      WHERE qda_usage.id = qda_layer_details.qda_usage_id
        AND qda_usage.user_id = auth.uid()
    )
  );

-- =============================================================================
-- VIEWS (for analytics)
-- =============================================================================

-- View: Daily QDA cost per user
CREATE OR REPLACE VIEW public.qda_daily_cost_per_user AS
SELECT
  user_id,
  DATE(created_at) as date,
  COUNT(*) as query_count,
  SUM(total_cost) as total_cost,
  AVG(total_cost) as avg_cost_per_query,
  AVG(complexity_score) as avg_complexity,
  AVG(total_time_ms) as avg_time_ms
FROM public.qda_usage
GROUP BY user_id, DATE(created_at)
ORDER BY date DESC;

-- View: Layer activation frequency
CREATE OR REPLACE VIEW public.qda_layer_activation_stats AS
SELECT
  highest_layer_used,
  COUNT(*) as activation_count,
  AVG(total_cost) as avg_cost,
  AVG(total_time_ms) as avg_time_ms,
  AVG(complexity_score) as avg_complexity
FROM public.qda_usage
GROUP BY highest_layer_used
ORDER BY activation_count DESC;

-- View: Polyvagal state distribution
CREATE OR REPLACE VIEW public.qda_polyvagal_distribution AS
SELECT
  polyvagal_state,
  COUNT(*) as query_count,
  AVG(stress_level) as avg_stress,
  AVG(complexity_score) as avg_complexity,
  AVG(total_cost) as avg_cost
FROM public.qda_usage
WHERE polyvagal_state IS NOT NULL
GROUP BY polyvagal_state
ORDER BY query_count DESC;

-- =============================================================================
-- FUNCTIONS (for analytics)
-- =============================================================================

-- Function: Get user's QDA usage summary
CREATE OR REPLACE FUNCTION public.get_user_qda_summary(
  p_user_id UUID,
  p_start_date TIMESTAMPTZ DEFAULT NOW() - INTERVAL '30 days',
  p_end_date TIMESTAMPTZ DEFAULT NOW()
)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_result JSON;
BEGIN
  SELECT json_build_object(
    'total_queries', COUNT(*),
    'total_cost', SUM(total_cost),
    'avg_cost_per_query', AVG(total_cost),
    'avg_complexity', AVG(complexity_score),
    'avg_time_ms', AVG(total_time_ms),
    'layer_distribution', json_object_agg(highest_layer_used, layer_count),
    'polyvagal_distribution', json_object_agg(polyvagal_state, state_count)
  )
  INTO v_result
  FROM (
    SELECT
      total_cost,
      complexity_score,
      total_time_ms,
      highest_layer_used,
      polyvagal_state,
      COUNT(*) OVER (PARTITION BY highest_layer_used) as layer_count,
      COUNT(*) OVER (PARTITION BY polyvagal_state) as state_count
    FROM public.qda_usage
    WHERE user_id = p_user_id
      AND created_at BETWEEN p_start_date AND p_end_date
  ) subquery;

  RETURN v_result;
END;
$$;

-- Function: Get system-wide QDA stats (admin only)
CREATE OR REPLACE FUNCTION public.get_system_qda_stats(
  p_start_date TIMESTAMPTZ DEFAULT NOW() - INTERVAL '30 days',
  p_end_date TIMESTAMPTZ DEFAULT NOW()
)
RETURNS JSON
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
  v_result JSON;
  v_is_admin BOOLEAN;
BEGIN
  -- Check if user is admin
  SELECT EXISTS (
    SELECT 1 FROM public.user_roles
    WHERE user_id = auth.uid() AND role = 'admin'
  ) INTO v_is_admin;

  IF NOT v_is_admin THEN
    RAISE EXCEPTION 'Unauthorized: Admin access required';
  END IF;

  SELECT json_build_object(
    'total_queries', COUNT(*),
    'unique_users', COUNT(DISTINCT user_id),
    'total_cost', SUM(total_cost),
    'avg_cost_per_query', AVG(total_cost),
    'avg_complexity', AVG(complexity_score),
    'strategen_activation_rate',
      (COUNT(*) FILTER (WHERE highest_layer_used = 'Strategen'))::FLOAT / COUNT(*),
    'critical_escalation_rate',
      (COUNT(*) FILTER (WHERE highest_layer_used = 'Vokteren'))::FLOAT / COUNT(*)
  )
  INTO v_result
  FROM public.qda_usage
  WHERE created_at BETWEEN p_start_date AND p_end_date;

  RETURN v_result;
END;
$$;

-- =============================================================================
-- GRANTS (permissions)
-- =============================================================================

-- Grant SELECT on views to authenticated users
GRANT SELECT ON public.qda_daily_cost_per_user TO authenticated;
GRANT SELECT ON public.qda_layer_activation_stats TO authenticated;
GRANT SELECT ON public.qda_polyvagal_distribution TO authenticated;

-- Grant EXECUTE on functions to authenticated users
GRANT EXECUTE ON FUNCTION public.get_user_qda_summary TO authenticated;
GRANT EXECUTE ON FUNCTION public.get_system_qda_stats TO authenticated;

-- =============================================================================
-- COMMENTS (documentation)
-- =============================================================================

COMMENT ON TABLE public.qda_usage IS 'Tracks QDA v2.0 usage, costs, and layer activation patterns';
COMMENT ON TABLE public.qda_layer_details IS 'Detailed tracking of individual layer processing (optional)';
COMMENT ON VIEW public.qda_daily_cost_per_user IS 'Daily QDA cost aggregated per user';
COMMENT ON VIEW public.qda_layer_activation_stats IS 'Frequency and cost stats by highest layer used';
COMMENT ON VIEW public.qda_polyvagal_distribution IS 'Query distribution across polyvagal states';
COMMENT ON FUNCTION public.get_user_qda_summary IS 'Get comprehensive QDA usage summary for a user';
COMMENT ON FUNCTION public.get_system_qda_stats IS 'Get system-wide QDA statistics (admin only)';

-- =============================================================================
-- END OF MIGRATION
-- =============================================================================

-- Example query to verify migration:
-- SELECT COUNT(*) FROM public.qda_usage;
-- SELECT * FROM public.qda_layer_activation_stats;
