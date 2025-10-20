-- NAV-LOSEN MVP - INITIAL DATABASE SCHEMA
-- Created: 20. oktober 2025
-- Author: Manus (Agent #6)
-- Description: Complete database schema for NAV-Losen MVP with data firewall

-- ============================================================================
-- PART 1: NAV-LOSEN DATA (Tvedestrand Pilot)
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table (NAV-Losen specific)
CREATE TABLE navlosen_users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    -- GDPR fields
    consent_given BOOLEAN DEFAULT FALSE,
    consent_date TIMESTAMPTZ,
    data_retention_until TIMESTAMPTZ,
    -- Metadata
    pilot_group TEXT DEFAULT 'tvedestrand',
    onboarding_completed BOOLEAN DEFAULT FALSE
);

-- Emotion check-ins (Mestringsside data)
CREATE TABLE navlosen_checkins (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES navlosen_users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    -- Mestringsside Fase 1-2: Quadrant selection
    quadrant TEXT NOT NULL CHECK (quadrant IN ('red', 'yellow', 'blue', 'green')),
    -- Mestringsside Fase 3: Emotion word
    emotion_word TEXT NOT NULL,
    emotion_definition TEXT,
    -- Mestringsside Fase 4a: Pressure and signals
    pressure_level INTEGER CHECK (pressure_level BETWEEN 1 AND 10),
    body_signals JSONB, -- Array of selected body signals
    -- Mestringsside Fase 5-6: Lira conversation
    lira_conversation_id UUID,
    -- Health Connect data (optional)
    health_data JSONB -- {steps, sleep_hours, heart_rate}
);

-- Lira conversations
CREATE TABLE navlosen_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES navlosen_users(id) ON DELETE CASCADE,
    checkin_id UUID REFERENCES navlosen_checkins(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    -- Conversation metadata
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'archived')),
    -- Messages stored as JSONB array
    messages JSONB DEFAULT '[]'::jsonb
);

-- Lira recommendations
CREATE TABLE navlosen_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES navlosen_conversations(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    -- Recommendation content
    recommendation_type TEXT CHECK (recommendation_type IN ('practice', 'music', 'resource')),
    title TEXT NOT NULL,
    description TEXT,
    content_url TEXT,
    -- User interaction
    viewed BOOLEAN DEFAULT FALSE,
    viewed_at TIMESTAMPTZ,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMPTZ
);

-- Mastery Log (user-saved strategies)
CREATE TABLE navlosen_mastery_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES navlosen_users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    -- Strategy content
    strategy_title TEXT NOT NULL,
    strategy_description TEXT,
    emotion_context TEXT, -- Which emotion this strategy helps with
    -- Effectiveness tracking
    times_used INTEGER DEFAULT 0,
    effectiveness_rating DECIMAL(3,2) -- 0.00 to 10.00
);

-- ============================================================================
-- PART 2: HOMO LUMEN DATA (R&D and Agent Learning)
-- ============================================================================

-- SMK (Symbiotisk Minne) entries
CREATE TABLE homo_lumen_smk (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    -- SMK metadata
    smk_type TEXT NOT NULL CHECK (smk_type IN ('LP', 'CS', 'EI', 'SMK')),
    smk_number INTEGER NOT NULL,
    agent_id TEXT NOT NULL, -- e.g., 'orion', 'lira', 'manus'
    -- SMK content
    title TEXT NOT NULL,
    description TEXT,
    content TEXT NOT NULL,
    tags JSONB DEFAULT '[]'::jsonb,
    -- Git integration
    git_commit_sha TEXT,
    git_file_path TEXT,
    -- Validation
    triadic_score DECIMAL(4,3), -- 0.000 to 1.000
    validated_by TEXT,
    validated_at TIMESTAMPTZ
);

-- Agent sessions (for tracking agent work)
CREATE TABLE homo_lumen_agent_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id TEXT NOT NULL,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    -- Session metadata
    session_type TEXT CHECK (session_type IN ('research', 'development', 'coordination', 'validation')),
    focus_area TEXT,
    -- Outcomes
    smk_entries_created INTEGER DEFAULT 0,
    decisions_made INTEGER DEFAULT 0,
    artifacts_created JSONB DEFAULT '[]'::jsonb
);

-- Design iterations (Nyra's work)
CREATE TABLE homo_lumen_design_iterations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    -- Design metadata
    component_name TEXT NOT NULL,
    iteration_number INTEGER NOT NULL,
    designer TEXT DEFAULT 'nyra',
    -- Design content
    description TEXT,
    figma_url TEXT,
    screenshot_url TEXT,
    -- Feedback
    feedback JSONB DEFAULT '[]'::jsonb,
    approved BOOLEAN DEFAULT FALSE,
    approved_by TEXT,
    approved_at TIMESTAMPTZ
);

-- ============================================================================
-- PART 3: DATA FIREWALL (CRITICAL FOR GDPR)
-- ============================================================================

-- Row Level Security (RLS) policies

-- NAV-Losen users can only see their own data
ALTER TABLE navlosen_users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own data" ON navlosen_users
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own data" ON navlosen_users
    FOR UPDATE USING (auth.uid() = id);

-- NAV-Losen check-ins
ALTER TABLE navlosen_checkins ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own checkins" ON navlosen_checkins
    FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users can insert own checkins" ON navlosen_checkins
    FOR INSERT WITH CHECK (user_id = auth.uid());

-- NAV-Losen conversations
ALTER TABLE navlosen_conversations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own conversations" ON navlosen_conversations
    FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users can insert own conversations" ON navlosen_conversations
    FOR INSERT WITH CHECK (user_id = auth.uid());

-- NAV-Losen recommendations
ALTER TABLE navlosen_recommendations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own recommendations" ON navlosen_recommendations
    FOR SELECT USING (
        conversation_id IN (
            SELECT id FROM navlosen_conversations WHERE user_id = auth.uid()
        )
    );

-- NAV-Losen mastery log
ALTER TABLE navlosen_mastery_log ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Users can view own mastery log" ON navlosen_mastery_log
    FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users can insert own mastery log" ON navlosen_mastery_log
    FOR INSERT WITH CHECK (user_id = auth.uid());
CREATE POLICY "Users can update own mastery log" ON navlosen_mastery_log
    FOR UPDATE USING (user_id = auth.uid());

-- Homo Lumen data is ONLY accessible to agents (not NAV-Losen users)
ALTER TABLE homo_lumen_smk ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Only agents can access SMK" ON homo_lumen_smk
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.uid() = id
            AND raw_user_meta_data->>'role' = 'agent'
        )
    );

ALTER TABLE homo_lumen_agent_sessions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Only agents can access sessions" ON homo_lumen_agent_sessions
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.uid() = id
            AND raw_user_meta_data->>'role' = 'agent'
        )
    );

ALTER TABLE homo_lumen_design_iterations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Only agents can access design iterations" ON homo_lumen_design_iterations
    FOR ALL USING (
        EXISTS (
            SELECT 1 FROM auth.users
            WHERE auth.uid() = id
            AND raw_user_meta_data->>'role' = 'agent'
        )
    );

-- ============================================================================
-- PART 4: INDEXES FOR PERFORMANCE
-- ============================================================================

-- NAV-Losen indexes
CREATE INDEX idx_navlosen_checkins_user_id ON navlosen_checkins(user_id);
CREATE INDEX idx_navlosen_checkins_created_at ON navlosen_checkins(created_at DESC);
CREATE INDEX idx_navlosen_conversations_user_id ON navlosen_conversations(user_id);
CREATE INDEX idx_navlosen_conversations_checkin_id ON navlosen_conversations(checkin_id);
CREATE INDEX idx_navlosen_recommendations_conversation_id ON navlosen_recommendations(conversation_id);
CREATE INDEX idx_navlosen_mastery_log_user_id ON navlosen_mastery_log(user_id);

-- Homo Lumen indexes
CREATE INDEX idx_homo_lumen_smk_agent_id ON homo_lumen_smk(agent_id);
CREATE INDEX idx_homo_lumen_smk_created_at ON homo_lumen_smk(created_at DESC);
CREATE INDEX idx_homo_lumen_smk_type ON homo_lumen_smk(smk_type);
CREATE INDEX idx_homo_lumen_agent_sessions_agent_id ON homo_lumen_agent_sessions(agent_id);
CREATE INDEX idx_homo_lumen_design_iterations_component ON homo_lumen_design_iterations(component_name);

-- ============================================================================
-- PART 5: FUNCTIONS AND TRIGGERS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_navlosen_users_updated_at
    BEFORE UPDATE ON navlosen_users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_navlosen_conversations_updated_at
    BEFORE UPDATE ON navlosen_conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_navlosen_mastery_log_updated_at
    BEFORE UPDATE ON navlosen_mastery_log
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_homo_lumen_smk_updated_at
    BEFORE UPDATE ON homo_lumen_smk
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to auto-delete user data after retention period (GDPR)
CREATE OR REPLACE FUNCTION delete_expired_user_data()
RETURNS void AS $$
BEGIN
    DELETE FROM navlosen_users
    WHERE data_retention_until < NOW();
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- PART 6: SEED DATA (FOR TESTING)
-- ============================================================================

-- Insert test agent user (for Homo Lumen access)
-- Note: This should be done via Supabase Auth UI or API, not directly in SQL
-- INSERT INTO auth.users (email, raw_user_meta_data) VALUES
-- ('orion@homolumen.ai', '{"role": "agent", "agent_id": "orion"}');

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================

-- Verification queries (run these after migration)
-- SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
-- SELECT * FROM navlosen_users LIMIT 1;
-- SELECT * FROM homo_lumen_smk LIMIT 1;

